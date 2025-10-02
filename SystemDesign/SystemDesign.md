# System Design Overview

This workspace consolidates system design reference notes. Each concept page stays lightweight for quick refreshes and uses diagrams to reinforce mental models.

## How to Use This Guide
1. Start here to recall interview approach, evaluation criteria, and core pillars.
2. Open any concept in `Components/` to see:
   - Quick Refresh summary
   - When to Reach For It use cases
   - Example Scenario (often with diagrams)
   - Visualization (Mermaid diagram)
   - Operational Guidance
   - Deepen Your Understanding (video/article links)
3. Document practice prompts in `Questions/` when ready.

## How to Approach Interviews
Requirements → CoreEntities → API/Interface → DataFlow → HighLevelDesign → Deep Dives.

## What Interviewers Evaluate
1. Problem Solving: Identify and prioritize core challenges.
2. Solution Design: Create scalable architectures with balanced trade-offs.
3. Technical Excellence: Demonstrate depth across systems topics.
4. Communication: Explain complex ideas clearly under time pressure.

## Core Pillars to Master
- Storage
- Scalability (compute + storage: sharding, consistent hashing)
- Networking (Layer 7 REST/GraphQL/gRPC, WebSockets/SSE; Layer 4 TCP vs UDP; Layer 3 load balancing, firewalls, ACLs)
- Latency, Throughput & Performance (memorize baseline access times: RAM ~100ns, SSD ~0.1–0.2ms, HDD ~1–2ms)
- Fault Tolerance & Redundancy
- CAP Theorem

## Concept Directory
- [APIDesign](Components/APIDesign.md)
- [APIProtocols](Components/APIProtocols.md)
- [APIGateways](Components/APIGateways.md)
- [BlobStorage](Components/BlobStorage.md)
- [BloomFilter](Components/BloomFilter.md)
- [Caching](Components/Caching.md)
- [CAPTheorem](Components/CAPTheorem.md)
- [CDNs](Components/CDNs.md)
- [ConsistentHashing](Components/ConsistentHashing.md)
- [CountMinSketch](Components/CountMinSketch.md)
- [DatabaseModels](Components/DatabaseModels.md)
- [DataPartitioning](Components/DataPartitioning.md)
- [Denormalization](Components/Denormalization.md)
- [HyperLogLog](Components/HyperLogLog.md)
- [Idempotency](Components/Idempotency.md)
- [Indexing](Components/Indexing.md)
- [LoadBalancing](Components/LoadBalancing.md)
- [MessageQueues](Components/MessageQueues.md)
- [RateLimiting](Components/RateLimiting.md)
- [Scalability](Components/Scalability.md)
- [Webhooks](Components/Webhooks.md)
- [WebSockets](Components/WebSockets.md)

## Useful Links
- Interview fast track: https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction
- Gaurav Sen – System Design Masterclass: https://youtu.be/Ru54dxzCyD0
- ByteByteGo – System Design Crash Course: https://youtu.be/IgyU0iFIoqM

## Folder Layout
```
SystemDesign/
├── Components/   # Each concept follows the standard template above
├── Questions/    # Practice prompts (see README inside)
└── SystemDesign.md
```

Add new concept pages in `Components/` using the same section order so they integrate seamlessly.