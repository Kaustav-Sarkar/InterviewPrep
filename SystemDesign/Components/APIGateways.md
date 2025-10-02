# APIGateways

## Quick Refresh
- Acts as a single ingress for microservices, handling routing, auth, rate limiting, and observability.
- Offloads cross-cutting concerns so backend services stay focused on business logic.
- Enables policy enforcement and protocol translation between clients and internal services.

## When to Reach For It
- You have many microservices and need consistent authentication, throttling, and logging.
- External partners require a simplified API surface while internal services proliferate.
- Migrating from a monolith to microservices and want centralized governance.

## Example Scenario
An e-commerce platform with web, mobile, and partner integrations:
- Gateway authenticates JWT tokens, applies rate limits, and routes product queries to dedicated services.
- Partners receive REST endpoints while internal clients use gRPC; the gateway performs protocol translation.
- Canary deployments are rolled out to a subset of traffic via gateway routing rules.

## Visualization
```mermaid
flowchart LR
    UserApp[User App<br/>(Web & Mobile)]
    PartnerApp[Partner App]
    APIGateway[API Gateway<br/>(Auth, Rate Limit, Logging)]
    ProductSvc[Product Service]
    OrderSvc[Order Service]
    InventorySvc[Inventory Service]
    Analytics[Analytics Sink]

    UserApp --> APIGateway
    PartnerApp --> APIGateway
    APIGateway --> ProductSvc
    APIGateway --> OrderSvc
    APIGateway --> InventorySvc
    APIGateway --> Analytics
```

## Operational Guidance
- Implement blue/green or canary releases by routing a percentage of traffic to new service versions.
- Keep business logic out of the gateway; delegate to downstream services.
- Instrument structured logs, tracing headers (e.g., `traceparent`), and per-route metrics.
- Cache configuration centrally (GitOps, service mesh control plane) to roll changes safely.

## Deepen Your Understanding
- Hello Interview – API Gateways: https://www.hellointerview.com/learn/system-design/api-gateway
- Gaurav Sen – API Gateway Patterns: https://youtu.be/16NIjk5H-ro
- ByteByteGo – API Gateway Explained: https://youtu.be/Gh5pFv5Zx6s
