# LFU Cache

## Quick Definition

Cache with Least Frequently Used eviction policy. Removes items with lowest access frequency when capacity is exceeded. Provides O(1) get/put operations.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Get | **O(1)** | O(capacity) |
| Put | **O(1)** | — |
| Eviction | **O(1)** | — |

## Core Operations

```java
class LFUCache {
    private int capacity;
    private int minFreq;
    private Map<Integer, Integer> keyToValue;
    private Map<Integer, Integer> keyToFreq;
    private Map<Integer, LinkedHashSet<Integer>> freqToKeys;
    
    public LFUCache(int capacity) {
        this.capacity = capacity;
        this.minFreq = 0;
        this.keyToValue = new HashMap<>();
        this.keyToFreq = new HashMap<>();
        this.freqToKeys = new HashMap<>();
    }
    
    public int get(int key) {
        if (!keyToValue.containsKey(key)) {
            return -1;
        }
        
        // Update frequency
        increaseFreq(key);
        return keyToValue.get(key);
    }
    
    public void put(int key, int value) {
        if (capacity <= 0) return;
        
        // Update existing key
        if (keyToValue.containsKey(key)) {
            keyToValue.put(key, value);
            increaseFreq(key);
            return;
        }
        
        // Check capacity
        if (keyToValue.size() >= capacity) {
            evictLFU();
        }
        
        // Add new key
        keyToValue.put(key, value);
        keyToFreq.put(key, 1);
        freqToKeys.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        minFreq = 1;
    }
    
    private void increaseFreq(int key) {
        int oldFreq = keyToFreq.get(key);
        int newFreq = oldFreq + 1;
        
        // Update frequency mapping
        keyToFreq.put(key, newFreq);
        
        // Remove from old frequency set
        freqToKeys.get(oldFreq).remove(key);
        
        // Add to new frequency set
        freqToKeys.computeIfAbsent(newFreq, k -> new LinkedHashSet<>()).add(key);
        
        // Update minFreq if necessary
        if (freqToKeys.get(oldFreq).isEmpty() && oldFreq == minFreq) {
            minFreq++;
        }
    }
    
    private void evictLFU() {
        // Get LFU key (first in insertion order for ties)
        int lfuKey = freqToKeys.get(minFreq).iterator().next();
        
        // Remove from all data structures
        freqToKeys.get(minFreq).remove(lfuKey);
        keyToFreq.remove(lfuKey);
        keyToValue.remove(lfuKey);
    }
}

// Simplified LFU using frequency counter
class SimpleLFUCache {
    private Map<Integer, Integer> cache;
    private Map<Integer, Integer> frequencies;
    private int capacity;
    
    public SimpleLFUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>();
        this.frequencies = new HashMap<>();
    }
    
    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        frequencies.merge(key, 1, Integer::sum);
        return cache.get(key);
    }
    
    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            cache.put(key, value);
            frequencies.merge(key, 1, Integer::sum);
            return;
        }
        
        if (cache.size() >= capacity) {
            evictLFU();
        }
        
        cache.put(key, value);
        frequencies.put(key, 1);
    }
    
    private void evictLFU() {
        int minFreq = frequencies.values().stream().min(Integer::compare).orElse(0);
        
        // Find first key with minimum frequency
        int keyToEvict = -1;
        for (int key : cache.keySet()) {
            if (frequencies.get(key) == minFreq) {
                keyToEvict = key;
                break;
            }
        }
        
        cache.remove(keyToEvict);
        frequencies.remove(keyToEvict);
    }
}

// Usage examples
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache: {1=1}
lfu.put(2, 2);   // cache: {1=1, 2=2}
lfu.get(1);      // returns 1, freq: {1=2, 2=1}
lfu.put(3, 3);   // evicts key 2, cache: {1=1, 3=3}
lfu.get(2);      // returns -1 (not found)
```

## Python Snippet

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity; self.minf = 0
        self.k2v = {}; self.k2f = {}
        self.f2keys = defaultdict(OrderedDict)
    def _touch(self, k):
        f = self.k2f[k]
        v = self.k2v[k]
        self.f2keys[f].pop(k, None)
        if not self.f2keys[f] and self.minf == f:
            self.minf += 1
        f += 1
        self.k2f[k] = f
        self.f2keys[f][k] = None
        return v
    def get(self, k):
        if k not in self.k2v: return -1
        return self._touch(k)
    def put(self, k, v):
        if self.cap <= 0: return
        if k in self.k2v:
            self.k2v[k] = v; self._touch(k); return
        if len(self.k2v) >= self.cap:
            # evict LFU: least-recently used within minf bucket
            evict_k, _ = self.f2keys[self.minf].popitem(last=False)
            self.k2v.pop(evict_k, None); self.k2f.pop(evict_k, None)
        self.k2v[k] = v; self.k2f[k] = 1; self.f2keys[1][k] = None; self.minf = 1
```

## When to Use

- Database buffer management
- Web proxy caches
- CPU cache replacement policies
- Memory management systems
- Long-running applications with varying access patterns

## Trade-offs

**Pros:**

- Good for workloads with temporal locality
- Adapts to changing access patterns
- O(1) operations with proper implementation
- Better than LRU for some scenarios

**Cons:**

- Complex implementation
- Higher memory overhead than LRU
- Cold start problem
- May not work well with scan patterns

## Practice Problems

- **LFU Cache**: Implement get() and put() in O(1) time
- **LRU Cache**: Compare with LFU implementation
- **Design Browser History**: Frequency-based page caching
- **File System Cache**: Implement with aging factor
- **Database Buffer Pool**: LFU with different eviction strategies

<details>
<summary>Implementation Notes (Advanced)</summary>

### Core Data Structures

- **Value storage**: HashMap for O(1) key-value access
- **Frequency tracking**: HashMap for key-frequency mapping
- **Frequency buckets**: Map from frequency to LinkedHashSet
- **Minimum frequency**: Track for efficient eviction

### Optimization Techniques

- **LinkedHashSet**: Maintains insertion order for tie-breaking
- **Frequency bucketing**: Groups keys by frequency
- **Lazy cleanup**: Clean empty frequency buckets as needed
- **Batch operations**: Process multiple updates together

### Variants and Extensions

- **Aging LFU**: Decay frequency over time
- **Windowed LFU**: Consider only recent access history
- **Adaptive**: Switch between LRU and LFU based on workload

### Performance Considerations

- **Memory overhead**: Multiple data structures increase space usage
- **Cache coherency**: Maintain consistency across structures
- **Hash function quality**: Critical for HashMap performance

</details>
