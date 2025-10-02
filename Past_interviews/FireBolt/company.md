# Must-Know Technical Concepts for Firebolt Interview

## Part 1: Complete Concept List

### Firebolt-Specific Concepts
1. Engine Architecture & Lifecycle
2. Multi-Dimensional Elasticity (Vertical, Horizontal, Concurrency Scaling)
3. Blue-Green Deployments for Engines
4. Decoupled Storage & Compute Architecture
5. F3 Storage Format & Sparse Indexing
6. Columnar Data Storage
7. Workload Isolation
8. Engine Types, Nodes, and Clusters
9. Primary, Aggregating, and Join Indexes

### Kubernetes & Container Orchestration
10. Kubernetes Engine Orchestration (EKS)
11. Karpenter Autoscaling
12. Cluster Autoscaler vs Karpenter
13. Horizontal Pod Autoscaler (HPA)
14. Kubernetes Node Pools
15. Pod Scheduling & Affinity
16. StatefulSets vs Deployments
17. ConfigMaps and Secrets Management
18. Kubernetes Operators
19. ArgoCD (GitOps)
20. Crossplane (Infrastructure as Code)

### Service Mesh & Networking
21. Service Mesh Architecture
22. Sidecar-less Service Mesh (eBPF/Cilium)
23. Pod-to-Pod Communication (L4 vs L7)
24. Service Discovery
25. Load Balancing Strategies
26. Network Policies
27. Multi-Cluster Communication
28. Traffic Routing & Gateway Patterns

### Distributed Systems Fundamentals
29. CAP Theorem
30. Eventual Consistency vs Strong Consistency
31. Distributed Consensus (Raft/Paxos concepts)
32. Leader Election
33. State Management in Distributed Systems
34. Fault Tolerance & High Availability
35. Circuit Breaker Pattern
36. Retry Strategies & Exponential Backoff
37. Idempotency

### Workflow Orchestration
38. Temporal Workflow Engine
39. Durable Execution
40. Event-Driven Architecture
41. State Machines vs Workflow Orchestration
42. Saga Pattern for Distributed Transactions
43. Task Queues
44. Workers & Activities in Temporal

### SRE & Observability
45. Four Golden Signals (Latency, Traffic, Errors, Saturation)
46. Prometheus Architecture & Data Model
47. Metrics, Logs, and Traces (Three Pillars)
48. Distributed Tracing (Jaeger/OpenTelemetry)
49. Service Level Objectives (SLOs) & Error Budgets
50. Alerting Strategies
51. Incident Response & On-Call
52. Chaos Engineering Basics

### Cloud Infrastructure (AWS/Multi-Cloud)
53. AWS EKS Architecture
54. AWS VPC & Networking
55. EC2 Instance Types & Selection
56. S3 Storage Classes
57. IAM Roles & Policies
58. Multi-Cloud Strategy (AWS, GCP, Azure)
59. Cloud Cost Optimization
60. Infrastructure as Code (Terraform)

### Data Warehouse Concepts
61. OLAP vs OLTP
62. Data Partitioning Strategies
63. Query Optimization & Execution Plans
64. Materialized Views
65. Data Compression Techniques
66. Data Pruning & Predicate Pushdown
67. Join Strategies (Hash, Merge, Nested Loop)
68. Aggregation Optimization

### Programming & System Design
69. Go Concurrency (Goroutines, Channels)
70. Python Async/Await
71. Database Connection Pooling
72. Caching Strategies (Write-through, Write-back)
73. Rate Limiting
74. Zero-Downtime Deployments
75. Rolling Updates vs Blue-Green vs Canary

---

## Part 2: Detailed Concepts (SDE3 Level)

### Core Job Responsibilities

#### 1. Engine Architecture & Lifecycle
**What it is**: Engines are Firebolt's compute resources that execute queries. The Engines team builds the orchestration layer that provisions, scales, monitors, and upgrades these compute clusters[docs:engine_fundamentals].[1]

**Key points**:
- Engines are **immutable clusters** - you don't patch them in place, you replace them
- Lifecycle states: STARTING → RUNNING → RESIZING → DRAINING → STOPPING → STOPPED[docs:engine_fundamentals]
- Engines are **decoupled from databases** - one engine can query multiple databases, one database can be queried by multiple engines
- Built on **Kubernetes pods** that run query execution workloads

**Why it matters**: The blog post mentions you'll work on "Engine provisioning services" - understanding the full lifecycle is critical[web_content_from_blog].

#### 2. Multi-Dimensional Elasticity
**What it is**: Firebolt engines can scale dynamically across **three dimensions simultaneously** without stopping[docs:engine_fundamentals].[1]

**Three dimensions**:
1. **Vertical Scaling**: Change node type (S/M/L/XL) - bigger machines for more power
2. **Horizontal Scaling**: Change number of nodes (1-128) - more machines for parallelism
3. **Concurrency Scaling**: Change number of clusters (MIN_CLUSTERS to MAX_CLUSTERS) - more independent clusters for concurrent queries

**Example**:
```sql
ALTER ENGINE MyEngine SET 
  TYPE = L              -- Vertical
  NODES = 8             -- Horizontal  
  MAX_CLUSTERS = 4;     -- Concurrency
```

**Why it matters**: This is a **key differentiator** vs competitors. You'll implement the infrastructure to make this work online without downtime[docs:engine_fundamentals].

#### 3. Blue-Green Deployments for Engines
**What it is**: A deployment strategy using **two identical environments** (Blue = current, Green = new) to achieve zero-downtime upgrades.[2][3]

**How Firebolt uses it**[web_content_from_blog]:
- When upgrading an engine, spin up a **new cluster** (Green) with the updated version
- Keep the **old cluster** (Blue) running and serving queries
- Once Green is ready and validated, **switch traffic** via the Gateway fleet
- Drain Blue gracefully, then terminate

**Implementation details**:
- Uses **immutable infrastructure** - never patch in place
- Traffic routing happens at **L4 (TCP)** level for fast switching
- Requires **health checks** on Green before switching
- Enables **instant rollback** by switching back to Blue

**Why it matters**: The blog explicitly mentions "zero-downtime upgrades" as a key feature you'll build[web_content_from_blog].

#### 4. Decoupled Storage & Compute Architecture
**What it is**: Storage and compute are **completely separated** - data lives in S3, compute engines read from it[docs:architecture].[1]

**Benefits**:
- **Independent scaling**: Add storage without adding compute, or vice versa
- **Cost efficiency**: Only pay for compute when queries run
- **Multiple engines share data**: Different workloads can use different engines on same data
- **No data movement**: Upgrading engines doesn't require data migration

**Architecture layers**[docs:architecture]:
1. **Storage Layer**: S3-based columnar storage with F3 format
2. **Compute Layer**: Ephemeral Kubernetes clusters (engines)
3. **Management Layer**: Metadata, security, observability

**Why it matters**: This architecture enables the multi-cloud expansion (GCP/Azure) the job description mentions[job_description].

### Kubernetes & Container Orchestration

#### 10. Kubernetes Engine Orchestration (EKS)
**What it is**: Amazon EKS is a managed Kubernetes service. Firebolt runs compute engines as **pods in EKS clusters**[web_content_from_blog].[4]

**Key concepts for Engines team**:
- **Control Plane**: Kubernetes API server, scheduler, controller manager (AWS manages this)
- **Worker Nodes**: EC2 instances that run your engine pods (you manage these)
- **Pod**: Smallest deployable unit - likely each engine node is a pod
- **Service**: Stable endpoint for accessing pods
- **Ingress/Gateway**: Entry point for external traffic

**Firebolt-specific patterns**[web_content_from_blog]:
- **Multi-cluster mesh**: Engines span multiple EKS clusters for high availability
- **Direct pod-to-pod communication**: Using sidecar-less mesh for low latency
- **Dynamic provisioning**: Engines created on-demand, not pre-allocated

**Why it matters**: The job description explicitly mentions "production experience with Kubernetes" as required[job_description].

#### 11. Karpenter Autoscaling
**What it is**: A **fast, intelligent** Kubernetes node autoscaler that provisions EC2 instances in <1 minute based on actual pod requirements.[5][4]

**How it works**:[6][4]
1. **Watches for unschedulable pods** (pods that can't fit on existing nodes)
2. **Analyzes pod requirements**: CPU, memory, GPU, storage, zone constraints
3. **Provisions right-sized nodes**: Launches EC2 instances that exactly match needs
4. **Bin-packing optimization**: Efficiently packs pods to minimize waste
5. **Deprovisioning**: Removes underutilized nodes automatically

**Karpenter vs Cluster Autoscaler**:[7][8]
- **Speed**: Karpenter is 10x faster (seconds vs minutes)
- **Flexibility**: Can provision different instance types dynamically vs fixed node groups
- **Cost**: Better bin-packing = fewer wasted nodes
- **Simplicity**: No need to configure Auto Scaling Groups

**Configuration example**:
```yaml
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
spec:
  requirements:
    - key: karpenter.sh/capacity-type
      operator: In
      values: ["spot", "on-demand"]
  limits:
    resources:
      cpu: 1000
      memory: 1000Gi
```

**Why it matters**: The blog post mentions **Karpenter** specifically as a tool used for autoscaling[web_content_from_blog].

#### 12. Cluster Autoscaler vs Karpenter
**Cluster Autoscaler (older approach)**:[8]
- Works with **Auto Scaling Groups** (pre-defined node configurations)
- Slower (5-10 minutes to add nodes)
- Less flexible (limited to ASG instance types)
- Reacts to pod failures/rescheduling

**Karpenter (modern approach)**:[4][7]
- Directly provisions **any EC2 instance type** that fits requirements
- Faster (30-60 seconds)
- Smarter bin-packing and consolidation
- Better cost optimization (can use Spot instances intelligently)

**When to use which**:
- **Cluster Autoscaler**: Simpler setups, predictable workloads, existing ASG infrastructure
- **Karpenter**: Dynamic workloads, cost optimization critical, need sub-minute scaling

**Why it matters**: You'll likely migrate or optimize Firebolt's autoscaling strategy for the multi-cloud expansion[job_description].

#### 18. Kubernetes Operators
**What it is**: Custom **controllers** that extend Kubernetes API to manage complex applications using **custom resources**.[4]

**How operators work**:
1. Define a **Custom Resource Definition (CRD)**: e.g., `FireboltEngine` resource
2. Write a **controller** (in Go) that watches for CRD changes
3. Controller **reconciles** desired state with actual state
4. Implements **domain-specific logic** (e.g., provisioning engine clusters)

**Example pattern**:
```yaml
apiVersion: firebolt.io/v1
kind: Engine
metadata:
  name: my-engine
spec:
  type: M
  nodes: 4
  clusters: 2
```

**Benefits**:
- **Declarative management**: Users declare what they want, operator figures out how
- **Self-healing**: Operator continuously reconciles state
- **Domain expertise encoded**: Complex workflows become simple resources

**Why it matters**: You'll likely build or extend operators to manage engine provisioning[job_description].

#### 19. ArgoCD (GitOps)
**What it is**: A **declarative GitOps** continuous delivery tool for Kubernetes that keeps cluster state in sync with Git repositories.[4]

**Core concepts**[job_description]:
- **Git as source of truth**: All Kubernetes manifests stored in Git
- **Automated sync**: ArgoCD continuously watches Git and applies changes
- **Drift detection**: Detects when cluster state diverges from Git
- **Rollback**: Easy rollback by reverting Git commits

**Workflow**:
1. Engineer commits Kubernetes manifests to Git
2. ArgoCD detects change
3. ArgoCD applies changes to cluster
4. ArgoCD monitors for drift and auto-heals

**Benefits**:
- **Auditability**: Every change tracked in Git history
- **Consistency**: Same deployment process across environments
- **Disaster recovery**: Can recreate entire cluster from Git

**Why it matters**: The job description lists ArgoCD experience as a bonus[job_description].

#### 20. Crossplane (Infrastructure as Code)
**What it is**: An **open-source Kubernetes extension** that lets you provision cloud infrastructure using Kubernetes-style YAML manifests[job_description].

**How it works**:
- Define **cloud resources as CRDs** (e.g., RDS database, S3 bucket, VPC)
- Crossplane controllers provision actual cloud resources via provider APIs
- Manage infrastructure with `kubectl` just like pods

**Example**:
```yaml
apiVersion: ec2.aws.crossplane.io/v1alpha1
kind: Instance
metadata:
  name: my-instance
spec:
  instanceType: m5.large
  ami: ami-12345
```

**Crossplane vs Terraform**:
- **Crossplane**: Kubernetes-native, continuous reconciliation, unified API
- **Terraform**: Standalone tool, explicit apply, mature ecosystem

**Why it matters**: Listed as desired experience for multi-cloud infrastructure management[job_description].

### Service Mesh & Networking

#### 22. Sidecar-less Service Mesh (eBPF/Cilium)
**What it is**: A **modern service mesh** that provides traffic management, security, and observability **without injecting sidecar proxies** into each pod.[9][10]

**Traditional service mesh (Istio)**:
- Injects **Envoy proxy sidecar** into every pod
- Sidecars intercept all traffic (adds latency)
- High resource overhead (2x pods running)
- Complex troubleshooting

**Sidecar-less approach (Cilium)**:[10][9]
- Uses **eBPF** (Extended Berkeley Packet Filter) in the Linux kernel
- **No sidecars** = lower latency, less resource usage
- **Node-level agents** handle networking for all pods on that node
- Direct pod-to-pod communication at **L4 (TCP/IP) level**

**eBPF explained**:
- Technology that runs sandboxed programs **in the Linux kernel**
- Can intercept network packets, system calls, function calls
- High performance (kernel-level, no context switching)
- Safe (verified programs, can't crash kernel)

**Firebolt's implementation**[web_content_from_blog]:
- Multi-cluster mesh with **direct pod-to-pod L4 communication**
- Avoids proxy overhead for ultra-low latency queries
- Likely uses Cilium or similar eBPF-based solution

**Why it matters**: The blog post emphasizes "sidecar-less multi-cluster mesh" as a key technology[web_content_from_blog].

#### 23. Pod-to-Pod Communication (L4 vs L7)
**Layer 4 (Transport Layer)**:[9]
- Operates at **TCP/UDP level**
- Routing based on **IP addresses and ports**
- **Low latency** (no parsing of application data)
- Limited visibility (can't inspect HTTP headers)

**Layer 7 (Application Layer)**:
- Operates at **HTTP/gRPC/etc. level**
- Routing based on **URL paths, headers, cookies**
- **Rich features** (retries, circuit breaking, authentication)
- Higher latency (requires parsing requests)

**Firebolt's choice**[web_content_from_blog]:
- Uses **L4** for engine-to-engine communication (speed is critical)
- Likely uses **L7** at the Gateway for external traffic (need routing logic)

**Why it matters**: Understanding this trade-off is key to designing the mesh architecture for multi-cloud[job_description].

### Distributed Systems Fundamentals

#### 29. CAP Theorem
**What it is**: In a distributed system with **network partitions**, you can only guarantee **two** of three properties: **Consistency**, **Availability**, **Partition Tolerance**.[11][12][13]

**Definitions**:[14][11]
- **Consistency (C)**: All nodes see the same data at the same time (every read gets the most recent write)
- **Availability (A)**: Every request gets a response (even if some nodes are down)
- **Partition Tolerance (P)**: System continues despite network failures between nodes

**Why you must choose**:
- Network partitions **will happen** in distributed systems (P is non-negotiable)
- During a partition, you must choose: **CP** (consistency) or **AP** (availability)

**CP systems** (choose consistency):[13]
- Return errors during partitions rather than stale data
- Examples: Banking, inventory systems, ticket booking
- Technologies: ZooKeeper, etcd, HBase

**AP systems** (choose availability):[13]
- Return potentially stale data during partitions
- Examples: Social media, content platforms, caching
- Technologies: Cassandra, DynamoDB, Riak

**Firebolt's position**:
- Engines: **AP** (availability over consistency for query execution)
- Metadata: **CP** (consistency critical for schema/config)

**Interview angle**: Discuss trade-offs for engine orchestration - do you prioritize engine availability (serve stale cluster state) or consistency (reject requests during network issues)?

#### 30. Eventual Consistency vs Strong Consistency
**Strong Consistency**:[11]
- **Guarantee**: Read always returns most recent write
- **How**: Synchronous replication, coordination between nodes
- **Cost**: Higher latency, lower availability during failures
- **Use case**: Financial transactions, inventory

**Eventual Consistency**:[12][11]
- **Guarantee**: If no new writes, eventually all nodes converge to same value
- **How**: Asynchronous replication, no coordination
- **Cost**: Potential stale reads, conflict resolution needed
- **Use case**: User profiles, analytics, caching

**BASE Model** (alternative to ACID):[12]
- **Basically Available**: System appears to work most of the time
- **Soft state**: State may change without input (due to eventual consistency)
- **Eventual consistency**: System will become consistent over time

**Firebolt application**:
- **Engine metadata**: Eventual consistency acceptable (brief staleness doesn't affect correctness)
- **Query results**: Strong consistency within a transaction
- **Cluster state propagation**: Eventual consistency for monitoring metrics

**Why it matters**: Multi-cloud deployments increase latency between regions - need to decide consistency guarantees[job_description].

#### 34. Fault Tolerance & High Availability
**Fault Tolerance**: System continues operating even when **components fail**.[15]

**High Availability**: System remains **operational** and **accessible** most of the time.[15]

**Techniques**:[15][4]
1. **Redundancy**: Multiple replicas of critical components
2. **Replication**: Data copied across nodes/regions
3. **Failover**: Automatic switch to backup when primary fails
4. **Health checks**: Continuous monitoring to detect failures
5. **Circuit breakers**: Stop cascading failures
6. **Graceful degradation**: Partial functionality when components fail

**Firebolt's HA strategy**[web_content_from_blog]:
- **Multi-cluster engines**: Spread across availability zones
- **Blue-green deployments**: Always have a backup cluster ready
- **Stateless engines**: Any engine can serve any query (no sticky state)
- **Draining**: Gracefully finish queries before stopping engines

**Measuring HA**:[16]
- **SLA (Service Level Agreement)**: External promise (e.g., 99.9% uptime)
- **SLO (Service Level Objective)**: Internal target (e.g., 99.95% uptime)
- **SLI (Service Level Indicator)**: Actual measurement (e.g., uptime last month)

**Why it matters**: Your on-call rotation will involve responding to availability incidents[job_description].

### Workflow Orchestration

#### 38. Temporal Workflow Engine
**What it is**: An **open-source microservices orchestration platform** that provides **durable execution** - workflows that survive failures, restarts, and infrastructure changes.[17][18][15]

**Core concepts**:[18][15]
- **Workflows**: Business logic that coordinates multiple steps (e.g., "Provision Engine")
- **Activities**: Individual tasks with business logic (e.g., "Launch EC2", "Register DNS")
- **Workers**: Processes that execute workflow and activity code
- **Task queues**: How Temporal distributes work to workers
- **Event history**: Complete log of everything that happened in a workflow

**How Temporal works**:[15]
1. **Client starts workflow**: `temporal.start_workflow("ProvisionEngine", params)`
2. **Temporal Server** persists workflow state to database
3. **Workers poll** task queues for work
4. **Activities execute**: Each step completes or fails with retries
5. **State persists**: After each activity, state saved
6. **Failures recover**: If worker crashes, another worker resumes from last checkpoint

**Key benefits**:[17][18]
- **Automatic retries**: Configure retry policies per activity
- **Timeouts**: Prevent stuck workflows
- **State tracking**: Don't lose progress on failures
- **Visibility**: Query workflow status, history
- **Versioning**: Deploy new workflow versions safely

**Example workflow** (pseudo-code):
```python
@workflow
def provision_engine(engine_id, node_type, node_count):
    cluster_id = await activity.launch_eks_cluster(node_type, node_count)
    await activity.configure_networking(cluster_id)
    await activity.deploy_engine_pods(cluster_id, engine_id)
    await activity.register_engine(engine_id, cluster_id)
    return cluster_id
```

**If this fails at step 3**: Temporal automatically resumes from step 3 on restart, no duplicate clusters launched.

**Why Firebolt uses it**[web_content_from_blog]:
- **Engine provisioning** is multi-step (launch nodes, configure mesh, deploy pods, register)
- **Upgrades** require coordination (launch new cluster, validate, switch traffic, drain old)
- **Must be reliable**: Can't leave half-provisioned engines

**Why it matters**: The blog post explicitly mentions Temporal for control plane workflows[web_content_from_blog].

#### 39. Durable Execution
**What it is**: The ability for a program to **survive failures** and **resume exactly where it left off**.[18][15]

**Traditional approach (fragile)**:
```python
def provision_engine():
    cluster = launch_cluster()  # Step 1
    # If crash here, we launched cluster but don't know cluster_id
    configure_network(cluster)  # Step 2
    # If crash here, have cluster but no networking
    register_engine(cluster)    # Step 3
```

**Problems**:
- **Lost state**: Variables (like `cluster_id`) lost on crash
- **Partial execution**: Cluster launched but not registered
- **No retry logic**: Manual intervention needed
- **Duplicate work**: Might launch second cluster on retry

**Durable execution approach** (with Temporal):[15]
```python
@workflow
def provision_engine():
    cluster = await activity.launch_cluster()  # State persisted here
    await activity.configure_network(cluster)  # State persisted here
    await activity.register_engine(cluster)    # State persisted here
```

**How it's durable**:[15]
- **After each `await`**: Temporal persists workflow state to database
- **On crash**: Workflow resumes from last `await`, variables intact
- **Retries**: Automatic retry of failed activities with exponential backoff
- **Exactly-once**: Each activity executes exactly once (no duplicates)

**Implementation details**:[15]
- Uses **event sourcing**: Every workflow action is an event
- **Replay**: On resume, Temporal replays event history to restore state
- **Deterministic code**: Workflow code must be deterministic for replay to work

**Why it matters**: Engine lifecycle management (provision, scale, upgrade, delete) requires durable workflows[web_content_from_blog].

### SRE & Observability

#### 45. Four Golden Signals (Latency, Traffic, Errors, Saturation)
**What it is**: Google's SRE methodology for **monitoring distributed systems** - focus on these four metrics for any service.[16]

**1. Latency**:[19][16]
- **What**: Time to serve a request
- **Why**: Slow = bad user experience
- **Metrics**: P50, P95, P99, P99.9 response times
- **Firebolt**: Query execution time, engine start time

**2. Traffic**:[19][16]
- **What**: Demand on your system
- **Why**: Understand load and capacity needs
- **Metrics**: Requests per second, concurrent queries
- **Firebolt**: Queries per second per engine, active engines

**3. Errors**:[19][16]
- **What**: Rate of failed requests
- **Why**: Indicates system health
- **Metrics**: HTTP 5xx rate, exception rate, failed query percentage
- **Firebolt**: Engine provisioning failures, query failures

**4. Saturation**:[16][19]
- **What**: How "full" your system is
- **Why**: Predict when you'll run out of capacity
- **Metrics**: CPU %, memory %, disk %, queue depth
- **Firebolt**: Node CPU/memory usage, engine queue length

**Why these four**:
- **Comprehensive**: Cover user-facing symptoms (latency, errors) and causes (traffic, saturation)
- **Actionable**: Each signal suggests specific remediation
- **Universal**: Apply to any service (database, API, batch job)

**Alerting strategy**:[16]
- **Symptom-based**: Alert on user-visible issues (high latency, high error rate)
- **Cause-based**: Monitor saturation for prediction, but don't wake up on-call

**Why it matters**: You'll be on-call and need to quickly diagnose issues[job_description].

#### 46. Prometheus Architecture & Data Model
**What it is**: An **open-source monitoring** system that collects, stores, and queries **time-series metrics**.[20][19]

**Architecture**:[20]
1. **Prometheus Server**: Scrapes and stores metrics
2. **Targets**: Services that expose `/metrics` endpoint
3. **Exporters**: Convert non-Prometheus metrics to Prometheus format
4. **Alertmanager**: Handles alerts (deduplication, grouping, routing)
5. **Grafana**: Visualization (typically used with Prometheus)

**How it works**:[20]
- **Pull model**: Prometheus scrapes metrics from targets (vs push)
- **Service discovery**: Auto-discovers targets (e.g., via Kubernetes API)
- **Scrape interval**: Typically every 15-30 seconds
- **Local storage**: TSDB (Time Series Database) on disk

**Data model**:[20]
- **Metric name**: e.g., `firebolt_engine_cpu_usage`
- **Labels**: Key-value pairs for dimensions, e.g., `{engine_id="eng_123", node="node_1"}`
- **Timestamp**: When sample was collected
- **Value**: Numeric value

**Example metric**:
```
firebolt_engine_cpu_usage{engine_id="eng_123", node="node_1"} 85.3 1678901234
```

**PromQL** (Prometheus Query Language):
```
# Average CPU across all nodes of an engine
avg(firebolt_engine_cpu_usage{engine_id="eng_123"})

# Rate of query errors over last 5 minutes
rate(firebolt_query_errors_total[5m])
```

**Why Firebolt uses it**[web_content_from_blog]:
- Monitor engine metrics (CPU, memory, query count)
- Alert on abnormal behavior (high latency, OOM)
- Capacity planning (understand usage patterns)

**Why it matters**: The job description mentions "prometheus compatible observability stack"[job_description].

#### 48. Distributed Tracing (Jaeger/OpenTelemetry)
**What it is**: Tracking a **single request** as it flows through multiple services in a distributed system.[21][19]

**The problem**:
- User query hits Gateway → Metadata service → Engine → Storage
- Query is slow - which component is the bottleneck?
- Logs are fragmented across services

**How tracing works**:[21][19]
1. **Trace**: Entire journey of a request (e.g., one query)
2. **Span**: One operation within a trace (e.g., "parse SQL")
3. **Trace ID**: Unique ID propagated across all services
4. **Parent span ID**: Links spans into a tree

**Example trace structure**:
```
Trace ID: abc123
├─ Gateway (50ms)
│  └─ Parse Query (5ms)
├─ Metadata Service (20ms)
│  └─ Fetch Schema (15ms)
└─ Engine (300ms)
   ├─ Plan Query (10ms)
   └─ Execute Query (290ms)
      ├─ Read from S3 (200ms)  ← Bottleneck found!
      └─ Compute (90ms)
```

**OpenTelemetry**:[19]
- **Vendor-neutral standard** for traces, metrics, logs
- **SDKs** for instrumenting code (Go, Python, Java, etc.)
- **Collectors** for aggregating telemetry data
- **Exporters** to send data to backends (Jaeger, Zipkin, Datadog)

**Jaeger**:[21][19]
- **Open-source tracing backend** created by Uber
- Stores and visualizes traces
- Service dependency graph
- Root cause analysis

**Implementation**:
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def provision_engine(engine_id):
    with tracer.start_as_current_span("provision_engine"):
        with tracer.start_as_current_span("launch_cluster"):
            cluster = launch_cluster()
        with tracer.start_as_current_span("register_engine"):
            register(engine_id, cluster)
```

**Why it matters**: Debugging engine provisioning failures requires tracing across Temporal, Kubernetes, AWS APIs[web_content_from_blog].

### Cloud Infrastructure

#### 53. AWS EKS Architecture
**What it is**: Amazon Elastic Kubernetes Service - **managed Kubernetes control plane** on AWS.[4]

**Architecture components**:[4]
- **Control Plane** (AWS managed):
  - API Server: Handles all Kubernetes API requests
  - etcd: Stores cluster state
  - Scheduler: Assigns pods to nodes
  - Controller Manager: Runs controllers (replication, endpoints, etc.)
- **Data Plane** (you manage):
  - Worker Nodes: EC2 instances running kubelet
  - Pods: Your application containers
  - CNI Plugin: Networking (VPC CNI, Calico, Cilium)

**EKS-specific features**:[4]
- **IAM integration**: Use AWS IAM roles for pod authentication
- **VPC networking**: Pods get IPs from your VPC
- **Auto Mode** (new): Fully managed nodes and autoscaling
- **Fargate**: Serverless option (no EC2 management)

**Node types**:
- **Managed node groups**: AWS manages node lifecycle (patches, updates)
- **Self-managed nodes**: You manage everything
- **Fargate**: AWS manages everything, but more expensive

**Firebolt's likely setup**[web_content_from_blog]:
- **Multiple EKS clusters**: For high availability across AZs
- **Managed node groups**: With Karpenter for dynamic scaling
- **VPC CNI or Cilium**: For pod networking
- **IAM roles for service accounts**: Pods authenticate to AWS services

**Why it matters**: Core infrastructure you'll work with daily[job_description].

#### 58. Multi-Cloud Strategy (AWS, GCP, Azure)
**What it is**: Running workloads across **multiple cloud providers** rather than locking into one[job_description].

**Motivations**:
- **Customer requirements**: Some customers mandate GCP or Azure
- **Vendor lock-in avoidance**: Reduce dependence on single provider
- **Geographic coverage**: Different clouds excel in different regions
- **Cost optimization**: Leverage competitive pricing
- **Resilience**: Survive cloud-wide outages

**Challenges**:
- **Different APIs**: AWS vs GCP vs Azure have different primitives
- **Networking complexity**: Cross-cloud traffic is slow and expensive
- **Identity management**: Different IAM models
- **Operational overhead**: 3x the complexity
- **Cost**: Cross-cloud data transfer is expensive

**Firebolt's multi-cloud initiative**[job_description]:
- **Goal**: "Expand to GCP and Azure, building on existing AWS foundation"
- **Approach**: Likely use Kubernetes abstraction (runs on all clouds)
- **Challenges**:
  - Storage integration (S3 vs GCS vs Azure Blob)
  - Networking (VPC vs VNet vs VPC)
  - IAM (different for each cloud)
  - Cost management across clouds

**Technologies to enable multi-cloud**:
- **Kubernetes**: Same workload definition across clouds
- **Crossplane**: Manage cloud resources with Kubernetes CRDs
- **Terraform**: Write multi-cloud infrastructure as code
- **Service mesh**: Abstract networking across clouds

**Why it matters**: The job description explicitly calls out "bring Firebolt experience to GCP and Azure" as a key strategic initiative[job_description].

### Data Warehouse Concepts

#### 61. OLAP vs OLTP
**OLTP (Online Transaction Processing)**:
- **Purpose**: Day-to-day operations (e.g., e-commerce checkout)
- **Queries**: Simple, frequent writes and reads
- **Data**: Current, detailed records
- **Schema**: Normalized (3NF) to avoid redundancy
- **Example**: MySQL, PostgreSQL for application backend
- **Pattern**: `INSERT`, `UPDATE`, `DELETE`, simple `SELECT`

**OLAP (Online Analytical Processing)**:
- **Purpose**: Analytics and business intelligence
- **Queries**: Complex aggregations across large datasets
- **Data**: Historical, aggregated
- **Schema**: Denormalized (star/snowflake) for query speed
- **Example**: Firebolt, Snowflake, BigQuery
- **Pattern**: `SELECT ... GROUP BY ... JOIN ... WHERE`

**Why Firebolt is OLAP**:[22][23]
- Optimized for **read-heavy** analytical queries
- **Columnar storage** for efficient aggregations
- **Indexes** for fast filtering
- **Horizontal scaling** for large datasets
- Not designed for high-frequency writes

**Interview angle**: Discuss how engine architecture optimizes for OLAP workloads (parallelization, caching, indexing).

#### 63. Query Optimization & Execution Plans
**What it is**: The process of **transforming a SQL query** into the most efficient execution strategy.[24][25]

**Query execution stages**:[25]
1. **Parsing**: SQL text → Abstract Syntax Tree (AST)
2. **Analysis**: Validate schema, resolve table/column names
3. **Optimization**: Generate and compare execution plans
4. **Execution**: Run the chosen plan

**Optimization techniques**:[24]
- **Predicate pushdown**: Filter data as early as possible
- **Projection pushdown**: Only read needed columns (columnar storage helps!)
- **Join reordering**: Choose optimal join order (small tables first)
- **Index selection**: Use indexes to avoid full scans
- **Partition pruning**: Skip irrelevant partitions

**Example**:
```sql
SELECT customer_id, SUM(amount)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
```

**Bad plan**:
1. Read all orders
2. Filter by date
3. Group by customer

**Good plan**:
1. Use index on order_date to filter first
2. Only read customer_id and amount columns (columnar!)
3. Parallel group by across nodes

**Firebolt's advantages**:[26][22]
- **Sparse indexing**: Skip irrelevant data ranges
- **Aggregating indexes**: Pre-computed aggregations
- **Parallel execution**: Distribute work across nodes

**Why it matters**: Engine performance depends on query optimizer effectiveness.

#### 65. Data Compression Techniques
**Why compression matters**:
- **Storage cost**: S3 charges per GB stored
- **Network**: Less data to transfer from S3 to engines
- **Cache**: Fit more data in node memory cache
- **I/O**: Read fewer bytes from disk

**Common algorithms**[docs:architecture]:
- **LZ4**: Fast compression/decompression, moderate ratio (Firebolt likely uses this)
- **Zstd**: Better compression, slightly slower
- **Snappy**: Very fast, lower compression ratio
- **Parquet encoding**: Run-length, dictionary, bit-packing

**Columnar compression benefits**[docs:architecture]:[22]
- **Repetition**: Columns often have repeated values → run-length encoding
- **Sorted data**: Consecutive similar values compress better
- **Type-specific**: Integers compress differently than strings

**Example**:
```
Column: [USA, USA, USA, Canada, Canada, Mexico]
Run-length encoded: [(USA, 3), (Canada, 2), (Mexico, 1)]
Stored as: [USA, 3, Canada, 2, Mexico, 1]
```

**Trade-offs**:
- **Higher compression**: Lower storage, higher CPU to decompress
- **Lower compression**: Faster queries, higher storage cost

**Why it matters**: Firebolt's F3 format uses advanced compression for cost efficiency.[27][26]

---

## Interview Topics to Expect

### Technical Round 1: Coding (LeetCode-style)
- **Data structures**: Hash maps, heaps, trees
- **Algorithms**: Graph traversal, dynamic programming, sorting
- **Go specifics**: Goroutines, channels, error handling
- **Difficulty**: Medium to Hard (SDE3 level)

### Technical Round 2: System Design
**Likely questions**:
1. **Design Firebolt's engine provisioning system**
   - How would you provision 1000 engines per minute?
   - How to handle provisioning failures?
   - How to ensure no resource leaks?

2. **Design zero-downtime engine upgrades**
   - Blue-green or rolling update?
   - How to handle long-running queries?
   - How to validate new version before full rollback?

3. **Design autoscaling for engines**
   - Metrics to trigger scaling?
   - How fast can you scale?
   - How to avoid thrashing (scale up/down rapidly)?

### Technical Round 3: Infrastructure/SRE
- **Kubernetes**: Pod scheduling, resource limits, health checks
- **Observability**: What metrics to monitor for engines? Alerting strategy?
- **Incident response**: How to debug an engine that won't start?
- **Multi-cloud**: Challenges of running on AWS, GCP, Azure?

### Behavioral/Values
- **On-call experience**: How do you handle being woken up at 3am?
- **Collaboration**: Working with multiple teams (database, gateway, infra)?
- **Ambiguity**: How to approach problems without clear solutions?
- **Ownership**: Examples of taking end-to-end ownership

***

## Key Questions to Ask Them

1. **Technical**: What's the biggest technical challenge the Engines team faces today?
2. **Multi-cloud**: What's the timeline for GCP/Azure support? Which comes first?
3. **Scale**: How many engines are running in production today? Growth projections?
4. **Team**: How is the team structured? How many engineers in Bangalore vs Seattle?
5. **On-call**: What's the on-call schedule? Average incidents per week?
6. **Learning**: What opportunities to work with the core database team?
7. **Career**: What does growth look like for this role (Staff engineer path)?

***

## Final Preparation Tips

### In Next 2 Hours
1. **Review the blog post** again - ask questions about their specific architecture
2. **Sketch out** a blue-green deployment for Firebolt engines
3. **Practice explaining** CAP theorem and when to choose CP vs AP
4. **Memorize key metrics**: Four golden signals, engine lifecycle states
5. **Prepare examples** from your experience with distributed systems

### During Call
- **Ask clarifying questions** - shows thoughtful engineering
- **Think aloud** - they want to see your thought process
- **Draw diagrams** - helps communicate complex ideas
- **Connect to their product** - "This reminds me of how Firebolt does..."
- **Be honest** - "I haven't used Temporal, but here's how I'd approach it..."

Good luck! The fact that you're preparing this thoroughly shows the right mindset. Remember, they're not just evaluating technical knowledge, but how you think through problems and collaborate.