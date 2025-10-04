## Microservices Architecture

```mermaid
graph TD
    APIGateway[API gateway] --> ServiceA[Service A]
    APIGateway --> ServiceB[Service B]
    ServiceA --> DBA[(Service A database)]
    ServiceB --> DBB[(Service B database)]
    ServiceA --> EventBus[Event bus]
    ServiceB --> EventBus
    EventBus --> ServiceC[Service C]
```

### Core Principles

- Each service adheres to single responsibility and owns its data.
- Typical layers: application logic, dedicated datastore, API gateway, and event bus.

### Communication Patterns

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Service1
    participant Bus as Message bus
    participant Service2
    Client->>Gateway: Request
    Gateway->>Service1: Forward
    Service1->>Bus: Publish event
    Bus->>Service2: Consume event
    Service2-->>Client: Async result via callback or notification
```

- Prefer event/message buses for decoupled, resilient interaction.
- Direct HTTP chains risk cascading failures if any service is down.
- Explore CQRS and Event Sourcing for advanced patterns.

### REST Considerations

- POST requests can retrieve data when payloads are complex or must remain private.
- Understand and use appropriate HTTP error codes for robust APIs.
