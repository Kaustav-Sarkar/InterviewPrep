# APIDesign

## Quick Refresh
- Favor resource nouns for REST endpoints (`GET /events`), verbs for commands only when necessary.
- Choose pagination style (page/limit vs cursor) based on consistency and ordering needs.
- Design request/response contracts with clear status codes and error semantics.

## When to Reach For It
- Establishing a public-facing REST API with predictable contracts.
- Aligning microservices on shared standards for endpoints, pagination, and auth.
- Reviewing an existing API for interview scenarios to identify gaps.

## Example Scenario
Building an events service:
- `GET /events?city=NYC&date=2025-10-02` lists events filtered by city and date.
- `POST /events` (requires `@auth:admin`) creates a new event; respond with `201 Created` and the resource location.
- `PATCH /events/{id}` lets organizers update specific fields without overwriting the entire resource.
- Cursor pagination uses response fields like `nextCursor` to maintain ordering during high write volume.

## Visualizations
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Gateway
    participant EventService
    participant AuthService
    participant DB as EventStore (PostgreSQL)

    Client->>Gateway: POST /events (JWT)
    Gateway->>AuthService: Validate token & scopes
    AuthService-->>Gateway: Authorized (admin)
    Gateway->>EventService: CreateEvent command
    EventService->>DB: INSERT event payload
    DB-->>EventService: Ack
    EventService-->>Gateway: 201 Created + eventId
    Gateway-->>Client: 201 Created, Location header

    Client->>Gateway: GET /events?cursor=abc123
    Gateway->>EventService: FetchEvents(cursor)
    EventService->>DB: SELECT with cursor
    DB-->>EventService: Result page
    EventService-->>Gateway: Events + nextCursor
    Gateway-->>Client: 200 OK with pagination metadata
```

```mermaid
flowchart LR
    subgraph Contracts
        OpenAPI[[OpenAPI Spec]]
        Proto[[gRPC Proto Files]]
        GraphQLSDL[[GraphQL SDL]]
    end

    subgraph GatewayLayer
        RestGateway[REST Gateway]
        RpcGateway[gRPC Gateway]
        GraphQLGateway[GraphQL Gateway]
    end

    subgraph Services
        EventSvc[(Event Service)]
        SearchSvc[(Search Service)]
        BillingSvc[(Billing Service)]
    end

    Clients[[Clients]] --> RestGateway
    Clients --> RpcGateway
    Clients --> GraphQLGateway

    RestGateway --> EventSvc
    RpcGateway --> BillingSvc
    GraphQLGateway --> EventSvc
    GraphQLGateway --> SearchSvc
    GraphQLGateway --> BillingSvc

    OpenAPI -. governs .-> RestGateway
    Proto -. governs .-> RpcGateway
    GraphQLSDL -. governs .-> GraphQLGateway
```

## Operational Guidance
- Document HTTP methods, expected status codes, and idempotency guarantees in OpenAPI/Swagger specs.
- Mitigate GraphQL N+1 issues with batching (e.g., DataLoader) and field-level caching.
- For RPC between services, define versioned schemas and backward-compatible evolutions.
- Secure endpoints with JWT access tokens, mTLS, or API keys; advertise auth scopes in docs.

## Deepen Your Understanding
- Hello Interview – API Design: https://www.hellointerview.com/learn/system-design/in-a-hurry/apis
- Gaurav Sen – REST API Design Best Practices (2024): https://youtu.be/ZcSR5cX9G3U
- Hussein Nasser – Cursor Pagination Explained: https://youtu.be/v6oPtTh_zPk