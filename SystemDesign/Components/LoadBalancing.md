# LoadBalancing

## Quick Refresh
- Distributes incoming traffic across multiple servers to improve throughput, reduce latency, and increase resilience.
- Algorithms include Round Robin, Least Connections, and IP Hash for session affinity.
- Load balancers can be hardware, software proxies, or managed cloud services.

## When to Reach For It
- Scaling stateless application servers behind a single endpoint.
- Providing zero-downtime deployments via blue/green or rolling updates.
- Handling failover when backend instances crash or become unhealthy.

## Example Scenario
E-commerce web tier:
- Users hit a global anycast IP that routes to the nearest load balancer.
- Load balancer performs TLS termination, health checks, and forwards requests to healthy app servers.
- Weighted routing sends 5% of traffic to a canary deployment before full rollout.

## Visualization
```mermaid
graph LR
    Client[Client Requests]
    LB[Load Balancer<br/>(Health Checks, TLS, Routing)]
    App1[App Server A]
    App2[App Server B]
    App3[App Server C]

    Client --> LB
    LB --> App1
    LB --> App2
    LB --> App3
```

## Operational Guidance
- Configure health checks with sensible timeouts and retries before marking instances unhealthy.
- Ensure idempotent HTTP handlers so retried requests do not produce side effects.
- Use sticky sessions only when unavoidable; prefer externalizing session state.
- Monitor per-server load, error rates, and request latency to detect imbalances.

## Deepen Your Understanding
- Hello Interview – Load Balancers: https://www.hellointerview.com/learn/system-design/load-balancing
- Gaurav Sen – Load Balancer Design: https://youtu.be/sWEjqQ_pZ9Q
- ByteByteGo – Load Balancing Visualized: https://youtu.be/mjIX4W3YWpM
