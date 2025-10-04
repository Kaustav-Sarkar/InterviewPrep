## Networking Concepts

```mermaid
flowchart TD
    Router[Router or gateway]
    Switch[Switch]
    Devices[Local devices]
    Router --> Switch
    Switch --> Devices
    Router --> Internet
```

### Devices and Layers

- **Switch:** Connects devices within a network; Layer 2 (MAC-level) focus.
- **Router:** Connects different networks; Layer 3 routing between subnets/VLANs.
- **Default Gateway:** Switch/router address (e.g., `172.16.1.1`).
- **MAC Address:** Physical identifier assigned to a NIC.

### OSI Model Overview

| Layer | Name | Function |
| :--- | :--- | :--- |
| 7 | Application | HTTP/HTTPS, FTP; headers processed |
| 6 | Presentation | Formatting, encryption (HTTPS) |
| 5 | Session | Manages connections (often handled by client libraries) |
| 4 | Transport | Segments data; TCP/UDP |
| 3 | Network | Routes packets with source/destination IPs |
| 2 | Data Link | Frames data; MAC addressing; ARP |
| 1 | Physical | Signals across cables/fiber |

### IP Addressing

```mermaid
mindmap
  root((IP addressing))
    IPv4
      32-bit space
      Private ranges
      CIDR notation
    IPv6
      128-bit space
      Hexadecimal blocks
      Built-in IPsec
```

- **IPv4:** 32-bit addresses; private ranges include Class A (`10.0.0.0/8`), Class B (`172.16.0.0/12`), Class C (`192.168.0.0/16`).
- **CIDR & Subnets:** `/8` (large), `/24` (256 addresses). Usable host count is `2^(32 - CIDR) - 2`.
- **IPv6:** 128-bit hexadecimal; includes IPsec, autoconfiguration via router advertisement, optional DHCP.

### NAT and ARP

```mermaid
sequenceDiagram
    participant Device as Private device
    participant Router as NAT router
    participant Site as Internet site
    Device->>Router: Request (private IP and port)
    Router->>Router: Translate to public IP and port
    Router->>Site: Forward packet
    Site->>Router: Respond to public IP and port
    Router->>Device: Map back to private IP and port
```

- **ARP:** Broadcast to map IP → MAC within local network; never leaves LAN.
- **NAT:** Router rewrites private IP headers to its public IP, hides internal topology, maintains translation table.

### Mobile Networking & Hotspots

- SIM/eSIM authenticates device to the carrier.
- Hotspot mode mirrors router behavior: runs DHCP, uses NAT for connected clients.
- eSIMs store multiple profiles; modern phones keep two active numbers.

### VPN Fundamentals

```mermaid
flowchart LR
    Client[Client device]
    Client --> Tunnel[Encrypted tunnel]
    Tunnel --> VPNServer[VPN server]
    VPNServer --> Internet
    Internet --> VPNServer
    VPNServer --> Client
```

- VPN wraps original packets in encrypted tunnels (encapsulation) to a VPN server.
- Server replaces the client’s public IP with its own before forwarding traffic.
- VPNs do not block cookies by default; additional tools are needed.

### DNS Resolution

```mermaid
sequenceDiagram
    participant User
    participant BrowserCache as Browser cache
    participant OSCache as OS cache
    participant RouterCache as Router cache
    participant Resolver as Recursive resolver
    participant Root as Root server
    participant TLD as TLD server
    participant Auth as Authoritative server

    User->>BrowserCache: Lookup domain
    BrowserCache-->>User: Cache hit?
    User->>OSCache: Cache miss
    OSCache-->>User: Cache hit?
    User->>RouterCache: Cache miss
    RouterCache-->>User: Cache hit?
    RouterCache->>Resolver: Forward query
    Resolver->>Root: Request TLD servers
    Root-->>Resolver: Return TLD servers
    Resolver->>TLD: Request authoritative NS
    TLD-->>Resolver: Return authoritative NS
    Resolver->>Auth: Request final record
    Auth-->>Resolver: Return IP address
    Resolver-->>RouterCache: Cache result
    RouterCache-->>User: Provide IP
```

1. Browser cache → OS cache → router cache.
2. Recursive resolver (e.g., 8.8.8.8) queries root → TLD → authoritative nameserver.
3. Final IP returned and cached for reuse.

- **Record Types:** A (IPv4 address), CNAME (alias). Anycast IPs leverage BGP for shortest route to a shared address.

### DHCP

```mermaid
sequenceDiagram
    participant Device
    participant DHCP as DHCP Server
    Device->>DHCP: Discover
    DHCP-->>Device: Offer
    Device->>DHCP: Request
    DHCP-->>Device: Acknowledge (IP, Mask, Gateway, DNS, Lease)
```

- **DORA:** Discover → Offer → Request → Acknowledge.
- DHCP issues leases for IP, subnet mask, gateway, DNS.
- **APIPA:** Fallback `169.254.x.x` when DHCP fails; indicates connectivity issue.
- **Reservations:** Bind MAC addresses to specific IPs for predictable assignments.
