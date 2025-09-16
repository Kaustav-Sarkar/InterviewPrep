# Ordered Map (TreeMap)

## Quick Definition

Map that maintains keys in sorted order using a balanced binary search tree. Provides O(log n) operations with guaranteed ordering.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Put | **O(log n)** | O(n) |
| Get | **O(log n)** | — |
| Remove | **O(log n)** | — |
| Range Operations | O(log n + k) | — |

## Core Operations

```java
// Basic TreeMap operations
TreeMap<Integer, String> map = new TreeMap<>();

// Insertion maintains sorted order
map.put(30, "thirty");
map.put(10, "ten");
map.put(50, "fifty");
map.put(20, "twenty");
System.out.println(map);  // {10=ten, 20=twenty, 30=thirty, 50=fifty}

// Range operations
TreeMap<Integer, String> nums = new TreeMap<>();
nums.put(1, "one"); nums.put(3, "three"); nums.put(5, "five");
nums.put(7, "seven"); nums.put(9, "nine");

// Navigation methods
Integer firstKey = nums.firstKey();      // 1
Integer lastKey = nums.lastKey();        // 9
Integer lower = nums.lowerKey(5);        // 3 (largest < 5)
Integer floor = nums.floorKey(4);        // 3 (largest ≤ 4)
Integer ceiling = nums.ceilingKey(4);    // 5 (smallest ≥ 4)
Integer higher = nums.higherKey(5);      // 7 (smallest > 5)

// Range views
NavigableMap<Integer, String> subMap = nums.subMap(3, true, 7, false); // [3, 7)
NavigableMap<Integer, String> headMap = nums.headMap(5, false);         // < 5
NavigableMap<Integer, String> tailMap = nums.tailMap(5, true);          // ≥ 5

// Frequency map with ordering
String text = "hello world";
TreeMap<Character, Integer> charCount = new TreeMap<>();
for (char c : text.toCharArray()) {
    if (c != ' ') {
        charCount.merge(c, 1, Integer::sum);
    }
}
System.out.println(charCount);  // {d=1, e=1, h=1, l=3, o=2, r=1, w=1}

// Order statistics
class OrderStatistics {
    private TreeMap<Integer, Integer> valueToCount = new TreeMap<>();
    
    public void add(int value) {
        valueToCount.merge(value, 1, Integer::sum);
    }
    
    public int kthSmallest(int k) {
        int count = 0;
        for (Map.Entry<Integer, Integer> entry : valueToCount.entrySet()) {
            count += entry.getValue();
            if (count >= k) {
                return entry.getKey();
            }
        }
        throw new IllegalArgumentException("k too large");
    }
    
    public int rank(int value) {
        int rank = 0;
        for (Map.Entry<Integer, Integer> entry : valueToCount.entrySet()) {
            if (entry.getKey() >= value) break;
            rank += entry.getValue();
        }
        return rank + 1;  // 1-indexed
    }
}

// Interval scheduling
class IntervalScheduler {
    private TreeMap<Integer, Integer> intervals = new TreeMap<>();  // start -> end
    
    public boolean book(int start, int end) {
        Integer prevStart = intervals.floorKey(start);
        if (prevStart != null && intervals.get(prevStart) > start) {
            return false;  // overlap with previous
        }
        
        Integer nextStart = intervals.ceilingKey(start);
        if (nextStart != null && nextStart < end) {
            return false;  // overlap with next
        }
        
        intervals.put(start, end);
        return true;
    }
}
```

## Python Snippet

```python
# Use dict + sorted keys for range ops (or use 'sortedcontainers' for efficiency)
m = {30: "thirty", 10: "ten", 50: "fifty", 20: "twenty"}
for k in sorted(m.keys()): pass  # iteration in key order

def floor_key(m, x):
    ks = sorted(m)
    import bisect
    i = bisect.bisect_right(ks, x) - 1
    return ks[i] if i >= 0 else None

def ceiling_key(m, x):
    ks = sorted(m)
    import bisect
    i = bisect.bisect_left(ks, x)
    return ks[i] if i < len(ks) else None

def submap(m, lo, hi, lo_inc=True, hi_inc=False):
    ks = sorted(m); import bisect
    i = bisect.bisect_left(ks, lo) if lo_inc else bisect.bisect_right(ks, lo)
    j = bisect.bisect_right(ks, hi) if hi_inc else bisect.bisect_left(ks, hi)
    return {k: m[k] for k in ks[i:j]}
```

## When to Use

- Maintaining sorted key-value associations
- Range queries and ordered iteration
- Order statistics and rank queries
- Time-series data with timestamp keys
- Interval processing and scheduling

## Trade-offs

**Pros:**

- Keys always in sorted order
- Efficient range operations
- O(log n) guaranteed performance
- Rich navigation API

**Cons:**

- Slower than HashMap for basic operations
- Higher memory overhead
- Keys must be comparable
- No O(1) operations

## Practice Problems

- **Range Sum Query - Mutable**: Use TreeMap for coordinate compression
- **Meeting Rooms II**: TreeMap for interval scheduling
- **Count of Range Sum**: TreeMap with prefix sums
- **Sliding Window Median**: TreeMap for order statistics
- **Calendar Booking**: TreeMap for conflict detection

<details>
<summary>Implementation Notes (Advanced)</summary>

### TreeMap Internals

- **Red-Black Tree**: Java's TreeMap uses Red-Black tree implementation
- **Comparison**: Uses Comparable or Comparator for ordering
- **Null keys**: Not allowed (would break comparison)
- **Thread safety**: Not thread-safe, use ConcurrentSkipListMap for concurrency

### Performance Characteristics

- **Guaranteed O(log n)**: Unlike HashMap's amortized O(1)
- **Memory overhead**: Each node has color bit + 2 pointers
- **Cache locality**: Poor compared to arrays, better than general trees

### Navigation Operations

- **Range views**: SubMap, headMap, tailMap are live views
- **Descending operations**: Efficient reverse iteration
- **Null handling**: Methods return null for non-existent keys

</details>
