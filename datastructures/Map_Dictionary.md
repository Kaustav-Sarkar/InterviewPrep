# Map (Dictionary)

## Quick Definition

Key-value data structure providing fast lookups, insertions, and deletions. Maps unique keys to values with various implementation strategies.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Put | **O(1)** avg | O(n) |
| Get | **O(1)** avg | — |
| Remove | **O(1)** avg | — |
| Contains | **O(1)** avg | — |

## Core Operations

```java
// HashMap - most common implementation
HashMap<String, Integer> map = new HashMap<>();

// Basic operations
map.put("apple", 5);              // insert/update
Integer value = map.get("apple"); // retrieve: 5
Integer def = map.getOrDefault("banana", 0); // get with default: 0
boolean exists = map.containsKey("apple");   // check key existence
Integer removed = map.remove("apple");       // remove and return value

// Initialization options
HashMap<String, Integer> scores = new HashMap<>(Map.of(
    "Alice", 95, "Bob", 87, "Charlie", 92
));

// Advanced operations
map.putIfAbsent("orange", 10);           // insert only if key absent
map.merge("apple", 3, Integer::sum);     // merge with function
map.compute("grape", (k, v) -> v == null ? 1 : v + 1); // compute new value

// Different Map implementations
HashMap<String, Integer> hashMap = new HashMap<>();           // fast, no ordering
LinkedHashMap<String, Integer> linkedMap = new LinkedHashMap<>(); // insertion order
TreeMap<String, Integer> treeMap = new TreeMap<>();          // sorted by keys
ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>(); // thread-safe

// Frequency counting pattern
String text = "hello world";
Map<Character, Integer> charFreq = new HashMap<>();
for (char c : text.toCharArray()) {
    charFreq.merge(c, 1, Integer::sum);
}

// Two-sum problem solution
class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[0];
    }
}

// Caching pattern
class Cache {
    private Map<String, Integer> cache = new HashMap<>();
    
    public int calculate(String input) {
        return cache.computeIfAbsent(input, this::expensiveOperation);
    }
    
    private int expensiveOperation(String input) {
        return input.hashCode() % 1000;
    }
}

// Configuration management
class Config {
    private Map<String, String> properties = new HashMap<>();
    
    public String getString(String key, String defaultValue) {
        return properties.getOrDefault(key, defaultValue);
    }
    
    public int getInt(String key, int defaultValue) {
        String value = properties.get(key);
        return value != null ? Integer.parseInt(value) : defaultValue;
    }
}
```

## Python Snippet

```python
# Dict basics
m = {}
m["apple"] = 5
val = m.get("apple")
val_default = m.get("banana", 0)
exists = "apple" in m
removed = m.pop("apple", None)

# Initialization
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

# Advanced operations
m.setdefault("orange", 10)
m["apple"] = m.get("apple", 0) + 3
m["grape"] = (m.get("grape") or 0) + 1

# Two-sum
def two_sum(nums, target):
    mp = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in mp: return [mp[y], i]
        mp[x] = i
    return []

# Cache pattern
from functools import lru_cache
@lru_cache(maxsize=None)
def expensive(input_str):
    return hash(input_str) % 1000
```

## When to Use

- Fast key-value lookups and mappings
- Caching and memoization
- Frequency counting and statistics
- Indexing and search optimization
- Configuration and property management

## Trade-offs

**Pros:**

- Fast O(1) average operations
- Flexible key-value associations
- Rich set of implementations
- Excellent for caching patterns

**Cons:**

- O(n) worst-case for HashMap
- Memory overhead for hash table
- No ordering guarantee (HashMap)
- Hash function quality affects performance

## Practice Problems

- **Two Sum**: Classic HashMap application
- **Group Anagrams**: Map for efficient grouping
- **Valid Parentheses**: Stack with character mapping
- **First Unique Character**: Frequency counting
- **Design HashMap**: Implement from scratch

<details>
<summary>Implementation Notes (Advanced)</summary>

### HashMap Internals

- **Hash function**: Distributes keys across buckets
- **Collision resolution**: Chaining (Java 8+ uses trees for long chains)
- **Load factor**: Default 0.75 balances time vs space
- **Resize**: Doubles capacity when load factor exceeded

### Implementation Variants

- **HashMap**: Fast, no ordering
- **LinkedHashMap**: Maintains insertion/access order
- **TreeMap**: Sorted keys, O(log n) operations
- **ConcurrentHashMap**: Thread-safe with segments

### Performance Considerations

- **Hash quality**: Good distribution reduces collisions
- **Capacity planning**: Pre-size for known data
- **Memory overhead**: ~75% load factor means 25% empty space

</details>
