# LRU (Least Recently Used) Cache

## Problem Statement

Design an LRU (Least-Recently-Used) Cache that supports the following operations in O(1) average time:

- **get(key) → value**: If the key exists, return its value and mark the key as recently used; otherwise return -1 (or None/null depending on language).
- **put(key, value)**: Insert or update the (key, value). If the key already exists, update its value and mark it as recently used. If the cache reaches capacity, evict the least-recently-used entry before inserting.

The cache is initialized with a positive integer capacity `N`.

"Least recently used" refers to the entry whose `get`/`put` was farthest in the past.

## Examples

- **cap = 2**
  - put(1, "A") → {1:A}
  - put(2, "B") → {2:B, 1:A}  (2 most recent)
  - get(1) → "A"; order becomes {1:A, 2:B}
  - put(3, "C") → evicts key 2; cache {3:C, 1:A}
  - get(2) → -1 (evicted)
  - put(1, "D") → updates value of 1 and marks recent; cache {1:D, 3:C}

## Constraints & Notes

- **Capacity**: `1 <= N`
- Updates to an existing key must also mark it as recently used.
- If `N = 0`, every `put` becomes a no-op and every `get` returns `-1`.

## Solution Approach

To achieve strict O(1) for `get` and `put`, we combine:

- **Hash map** for O(1) key → node lookup.
- **Doubly linked list** to track recency order, with:
  - Head = most recent
  - Tail = least recent
- We use dummy **head** and **tail** sentinels to simplify adds/removes at the ends (no null checks at boundaries).

### Data Structures

- `Node { key, value, prev, next }`
- `DoublyLinkedList` supporting:
  - `addFirst(node)` → insert node right after head (mark most recent)
  - `remove(node)` → detach node from list in O(1)
  - `removeLast()` → detach and return node just before tail (LRU)
- `map: key → Node`

### Operations

- **get(key)**:
  - If key not in map, return `-1`.
  - Otherwise, move the node to the front (most recent) and return its value.

- **put(key, value)**:
  - If key exists: update node.value, move node to front.
  - Else:
    - If size == capacity: remove the LRU node (node before tail) and delete its key from map.
    - Create new node, add to front, store in map.

All steps are O(1) due to hash lookup and constant-time list operations.

## Reference Implementation (Python-like pseudocode)

```python
class Node:
    def __init__(self, k, v):
        self.k = k
        self.v = v
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}  # key -> Node
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    # internal helpers
    def _add_first(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node: Node) -> None:
        p, n = node.prev, node.next
        p.next = n
        n.prev = p

    def _remove_last(self) -> Node:
        lru = self.tail.prev
        if lru is self.head:
            return None
        self._remove(lru)
        return lru

    # API
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_first(node)
        return node.v

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.v = value
            self._remove(node)
            self._add_first(node)
            return

        if len(self.map) == self.cap:
            lru = self._remove_last()
            if lru is not None:
                self.map.pop(lru.k, None)

        node = Node(key, value)
        self._add_first(node)
        self.map[key] = node
```

## Correctness & Invariants

- The doubly linked list always represents items from most recent (after head) to least recent (before tail).
- Every node in the list has a corresponding entry in `map`, and vice versa.
- After `get`/`put`, the accessed/inserted key is moved to the front.
- When at capacity, eviction always removes the node right before tail (LRU).

## Complexity

- **Time**: `get` = O(1), `put` = O(1)
- **Space**: O(N) for up to N nodes plus hash map entries

## Common Pitfalls

- Forgetting to move an updated key to the front after `put`.
- Not removing the evicted key from the hash map.
- Mishandling edge cases when the list becomes empty (use sentinels to avoid).
- Capacity `N = 0` behavior: all gets return `-1`; puts are effectively no-ops.

## Variants & Extensions

- **LFU Cache**: Track frequency counts with an LRU list per frequency bucket.
- **Thread-safe LRU**: Guard operations with a mutex or use concurrent primitives.
- **TTL/Expiration**: Associate timestamps; evict if expired even if recently used.
- **Distributed LRU**: Shard keys via consistent hashing; each shard maintains a local LRU.

