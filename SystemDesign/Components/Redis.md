## Redis Overview

Redis is an in-memory data structure server optimized for low-latency access and rich data primitives. It can operate as a cache, primary database, or message broker depending on configuration and persistence strategy.[^v1]

### Core Characteristics

- **In-memory with optional persistence:** Keeps working data in RAM while offering Append-Only File (AOF) or snapshot (RDB) persistence to disk.[^v2]
- **Single-threaded event loop:** Uses a single-threaded architecture with cooperative multitasking, ensuring consistent performance when commands remain O(1) or O(log n).
- **Rich data types:** Strings, hashes, lists, sets, sorted sets, streams, bitmaps, HyperLogLog, and geospatial indexes provide expressive modeling without multiple systems.[^v3]
- **Client protocols:** Supports RESP (text-based) and RESP3 for structured responses, making it easy to use from any language.

### Memory-Resident Data Structures

| Data Type | Typical Use Cases | Key Commands |
| :--- | :--- | :--- |
| **String** | Counters, tokens, JSON blobs | `GET`, `SET`, `INCRBY`, `MGET` |
| **Hash** | User profiles, metadata maps | `HSET`, `HGETALL`, `HINCRBY` |
| **List** | Queues, recent activity feeds | `LPUSH`, `RPOP`, `LRANGE` |
| **Set** | Unique tag collections, de-duplication | `SADD`, `SISMEMBER`, `SUNION` |
| **Sorted Set** | Leaderboards, ranking, scheduling | `ZADD`, `ZRANGE`, `ZREVRANK` |
| **Stream** | Event sourcing, change data capture | `XADD`, `XREADGROUP` |

### Caching Patterns

- **Cache-Aside (Lazy Loading):** Application checks Redis first, then loads from the database and populates Redis on miss. Use TTL to prevent stale data.[^v1]
- **Write-Through:** Writes go through Redis and the backing store simultaneously, ensuring consistency but with higher write latency.
- **Write-Behind:** Buffer writes in Redis and flush asynchronously; ideal for amortizing heavy operations but requires durable persistence safeguards.

### Persistence & Durability Settings

- **RDB Snapshots:** Periodically dump the entire dataset to disk (`SAVE`, `BGSAVE`). Low overhead, but risk of data loss equal to snapshot interval.
- **AOF:** Append every write command to disk for near-zero data loss. Combine with `AOF rewrite` to control file size.
- **Hybrid:** Use both RDB and AOF for faster restarts plus stronger durability.
- **Replication:** Deploy replicas for read scaling and failover; replicas can be promoted automatically using Redis Sentinel.[^v2]

### High Availability & Scaling

- **Redis Sentinel:** Monitors masters and replicas, performs automatic failover, and updates clients with new topology.[^v3]
- **Redis Cluster:** Shards data across multiple nodes via hash slots (0–16383). Provides automatic partitioning, replication, and failover.
- **Proxy Solutions:** Twemproxy or Redis Cluster-aware clients can handle sharding logic externally when clusters are undesirable.

### Observability & Operations

- Monitor **memory fragmentation** and **eviction rates** (`INFO memory`).
- Choose eviction policies (`volatile-lru`, `allkeys-lfu`, etc.) based on workload characteristics.
- Use `SLOWLOG` to catch expensive commands; optimize data modeling to keep operations sub-millisecond.
- Apply ACLs (`ACL SETUSER`) to enforce least privilege access.

### Example Workflow

```bash
# Start a local Redis server (default port 6379)
redis-server

# Write/read simple data
redis-cli SET session:123 "user42"
redis-cli GET session:123

# Work with a leaderboard
redis-cli ZADD leaderboard 100 "playerA"
redis-cli ZADD leaderboard 120 "playerB"
redis-cli ZREVRANGE leaderboard 0 1 WITHSCORES

# Configure persistence
redis-cli CONFIG SET save "900 1 300 10"
redis-cli CONFIG SET appendonly yes
```

### When to Use Redis

- Sub-millisecond latency required for session stores, feature flags, or personalization.
- Real-time analytics with sliding windows, counters, or leaderboards.
- Message queues or pub/sub for lightweight event distribution.
- Rate limiting and distributed locks (`SETNX` + expirations) when managed carefully.

### Common Pitfalls

- **Unbounded keys:** Allowing lists or sets to grow indefinitely can trigger memory spikes leading to eviction or swap.
- **Blocking commands:** Avoid operations like `KEYS *` or `HGETALL` on huge structures in production.
- **Persistence mismatch:** Ensure durability settings match business expectations; default configuration might not survive restarts.
- **Network partitioning:** In cluster mode, understand the impact of losing quorum and configure `cluster-require-full-coverage` appropriately.

[^v1]: [Introduction to Redis concepts and caching strategies](https://youtu.be/Vx2zPMPvmug)
[^v2]: [Deep dive into Redis persistence and high availability](https://youtu.be/fmT5nlEkl3U)
[^v3]: [Advanced Redis data structures and clustering](https://youtu.be/OqCK95AS-YE)
