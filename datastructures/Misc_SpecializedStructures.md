# Misc Specialized Structures

## Quick Definition

Collection of purpose-built data structures for specific problem domains including geometric points, intervals, pairs/tuples, custom containers, and problem-specific optimized structures. Essential for competitive programming and specialized applications.

## Big-O Summary

| Structure | Access | Insert | Delete | Space | Use Case |
|-----------|--------|--------|--------|-------|-----------|
| Pair/Tuple | O(1) | O(1) | N/A | O(1) | Key-value, coordinates |
| Point2D/3D | O(1) | N/A | N/A | O(1) | Geometry problems |
| Interval | O(1) | N/A | N/A | O(1) | Range representations |
| MinMaxStack | O(1) | O(1) | O(1) | O(n) | Range queries on stack |
| Polynomial | O(1) | O(1) | O(n) | O(n) | Mathematical operations |

*Operations vary by specific structure implementation

## Core Operations

```java
import java.util.*;
import java.util.stream.Collectors;

// 1. Pair/Tuple for key-value pairs and coordinates
class Pair<T, U> {
    public final T first;
    public final U second;
    
    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Pair)) return false;
        Pair<?, ?> other = (Pair<?, ?>) obj;
        return Objects.equals(first, other.first) && Objects.equals(second, other.second);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(first, second);
    }
    
    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}

// 2. Point classes for geometry problems
class Point2D {
    public final double x, y;
    
    public Point2D(double x, double y) {
        this.x = x;
        this.y = y;
    }
    
    public double distanceTo(Point2D other) {
        double dx = x - other.x;
        double dy = y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    public Point2D add(Point2D other) {
        return new Point2D(x + other.x, y + other.y);
    }
    
    public Point2D subtract(Point2D other) {
        return new Point2D(x - other.x, y - other.y);
    }
    
    @Override
    public String toString() {
        return String.format("(%.2f, %.2f)", x, y);
    }
}

// 3. Interval/Range class for range problems
class Interval {
    public final int start, end;
    
    public Interval(int start, int end) {
        this.start = start;
        this.end = end;
    }
    
    public boolean overlaps(Interval other) {
        return start < other.end && other.start < end;
    }
    
    public boolean contains(int point) {
        return start <= point && point < end;
    }
    
    public int length() {
        return end - start;
    }
    
    public Interval intersect(Interval other) {
        int newStart = Math.max(start, other.start);
        int newEnd = Math.min(end, other.end);
        return newStart < newEnd ? new Interval(newStart, newEnd) : null;
    }
    
    @Override
    public String toString() {
        return "[" + start + ", " + end + ")";
    }
}

// 4. MinMax Stack - stack with O(1) min/max queries
class MinMaxStack<T extends Comparable<T>> {
    private Stack<T> stack = new Stack<>();
    private Stack<T> minStack = new Stack<>();
    private Stack<T> maxStack = new Stack<>();
    
    public void push(T item) {
        stack.push(item);
        
        if (minStack.isEmpty() || item.compareTo(minStack.peek()) <= 0) {
            minStack.push(item);
        }
        
        if (maxStack.isEmpty() || item.compareTo(maxStack.peek()) >= 0) {
            maxStack.push(item);
        }
    }
    
    public T pop() {
        if (stack.isEmpty()) throw new EmptyStackException();
        
        T item = stack.pop();
        
        if (item.equals(minStack.peek())) {
            minStack.pop();
        }
        
        if (item.equals(maxStack.peek())) {
            maxStack.pop();
        }
        
        return item;
    }
    
    public T getMin() {
        if (minStack.isEmpty()) throw new EmptyStackException();
        return minStack.peek();
    }
    
    public T getMax() {
        if (maxStack.isEmpty()) throw new EmptyStackException();
        return maxStack.peek();
    }
    
    public boolean isEmpty() {
        return stack.isEmpty();
    }
}

// 5. Frequency Counter - enhanced counting
class FrequencyCounter<T> {
    private Map<T, Integer> counts = new HashMap<>();
    private Map<Integer, Set<T>> freqToItems = new HashMap<>();
    private int maxFreq = 0;
    
    public void add(T item) {
        int oldFreq = counts.getOrDefault(item, 0);
        int newFreq = oldFreq + 1;
        
        counts.put(item, newFreq);
        
        // Update frequency mappings
        if (oldFreq > 0) {
            freqToItems.get(oldFreq).remove(item);
            if (freqToItems.get(oldFreq).isEmpty()) {
                freqToItems.remove(oldFreq);
            }
        }
        
        freqToItems.computeIfAbsent(newFreq, k -> new HashSet<>()).add(item);
        maxFreq = Math.max(maxFreq, newFreq);
    }
    
    public int getCount(T item) {
        return counts.getOrDefault(item, 0);
    }
    
    public Set<T> getMostFrequent() {
        return freqToItems.getOrDefault(maxFreq, Collections.emptySet());
    }
    
    public Set<T> getItemsWithFrequency(int freq) {
        return freqToItems.getOrDefault(freq, Collections.emptySet());
    }
}

// 6. LRU with TTL (Time To Live)
class TTLCache<K, V> {
    private static class Node<K, V> {
        K key;
        V value;
        long expiryTime;
        Node<K, V> prev, next;
        
        Node(K key, V value, long expiryTime) {
            this.key = key;
            this.value = value;
            this.expiryTime = expiryTime;
        }
    }
    
    private Map<K, Node<K, V>> cache = new HashMap<>();
    private Node<K, V> head = new Node<>(null, null, 0);
    private Node<K, V> tail = new Node<>(null, null, 0);
    private int capacity;
    private long defaultTTL;
    
    public TTLCache(int capacity, long defaultTTL) {
        this.capacity = capacity;
        this.defaultTTL = defaultTTL;
        head.next = tail;
        tail.prev = head;
    }
    
    public V get(K key) {
        Node<K, V> node = cache.get(key);
        if (node == null || System.currentTimeMillis() > node.expiryTime) {
            if (node != null) {
                removeNode(node);
                cache.remove(key);
            }
            return null;
        }
        moveToHead(node);
        return node.value;
    }
    
    public void put(K key, V value) {
        put(key, value, defaultTTL);
    }
    
    public void put(K key, V value, long ttl) {
        long expiryTime = System.currentTimeMillis() + ttl;
        Node<K, V> existing = cache.get(key);
        
        if (existing != null) {
            existing.value = value;
            existing.expiryTime = expiryTime;
            moveToHead(existing);
        } else {
            Node<K, V> newNode = new Node<>(key, value, expiryTime);
            cache.put(key, newNode);
            addToHead(newNode);
            
            if (cache.size() > capacity) {
                Node<K, V> last = tail.prev;
                removeNode(last);
                cache.remove(last.key);
            }
        }
    }
    
    private void addToHead(Node<K, V> node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }
}

// Usage examples
// Pair usage
Pair<String, Integer> coordinate = new Pair<>("x", 10);
Map<Pair<Integer, Integer>, String> grid = new HashMap<>();
grid.put(new Pair<>(0, 0), "origin");

// Point2D usage
Point2D p1 = new Point2D(0, 0);
Point2D p2 = new Point2D(3, 4);
System.out.println("Distance: " + p1.distanceTo(p2)); // 5.0

// Interval usage
Interval meeting1 = new Interval(9, 11);
Interval meeting2 = new Interval(10, 12);
System.out.println("Overlap: " + meeting1.overlaps(meeting2)); // true

// MinMaxStack usage
MinMaxStack<Integer> stack = new MinMaxStack<>();
stack.push(3); stack.push(1); stack.push(4);
System.out.println("Min: " + stack.getMin() + ", Max: " + stack.getMax()); // Min: 1, Max: 4

// FrequencyCounter usage
FrequencyCounter<String> counter = new FrequencyCounter<>();
counter.add("apple"); counter.add("banana"); counter.add("apple");
System.out.println("Most frequent: " + counter.getMostFrequent()); // [apple]
```

## Python Snippet

```python
from collections import Counter, OrderedDict
from dataclasses import dataclass
import time

# 1. Pair as tuple and simple usage
Pair = tuple  # (first, second)

# 2. Point2D
@dataclass(frozen=True)
class Point2D:
    x: float; y: float
    def distance_to(self, o):
        dx, dy = self.x - o.x, self.y - o.y
        return (dx*dx + dy*dy) ** 0.5

# 3. Interval
@dataclass(frozen=True)
class Interval:
    start: int; end: int
    def overlaps(self, o): return self.start < o.end and o.start < self.end
    def contains(self, p): return self.start <= p < self.end
    def intersect(self, o):
        s, e = max(self.start, o.start), min(self.end, o.end)
        return Interval(s, e) if s < e else None

# 4. MinMaxStack
class MinMaxStack:
    def __init__(self): self.s=[]; self.mins=[]; self.maxs=[]
    def push(self, x):
        self.s.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
        self.maxs.append(x if not self.maxs else max(x, self.maxs[-1]))
    def pop(self):
        self.mins.pop(); self.maxs.pop(); return self.s.pop()
    def get_min(self): return self.mins[-1]
    def get_max(self): return self.maxs[-1]

# 5. FrequencyCounter
class FrequencyCounter:
    def __init__(self): self.c = Counter()
    def add(self, x): self.c[x]+=1
    def count(self, x): return self.c[x]
    def most_frequent(self):
        mx = max(self.c.values(), default=0)
        return {k for k,v in self.c.items() if v==mx}

# 6. TTLCache (LRU + expiration)
class TTLCache(OrderedDict):
    def __init__(self, capacity, default_ttl_ms):
        super().__init__(); self.cap=capacity; self.ttl=default_ttl_ms
    def _expired(self, exp): return time.time()*1000 > exp
    def get(self, k, default=None):
        v = super().get(k, None)
        if v is None: return default
        val, exp = v
        if self._expired(exp):
            super().pop(k, None); return default
        self.move_to_end(k); return val
    def put(self, k, v, ttl_ms=None):
        exp = time.time()*1000 + (ttl_ms if ttl_ms is not None else self.ttl)
        super().__setitem__(k, (v, exp)); self.move_to_end(k)
        if len(self) > self.cap: self.popitem(last=False)
```

## When to Use

- **Pair/Tuple**: Coordinate pairs, key-value associations, returning multiple values
- **Point2D/3D**: Computational geometry, graphics, spatial algorithms
- **Interval**: Meeting scheduling, range queries, timeline problems
- **MinMaxStack**: Range queries on sequential data with stack operations
- **FrequencyCounter**: Real-time frequency analysis, most frequent item queries
- **TTLCache**: Session management, temporary data storage, time-based invalidation

## Trade-offs

**Pros:**

- Purpose-built for specific problem domains
- Often provide optimal complexity for target operations
- Clean abstractions reduce code complexity
- Encapsulate domain-specific logic
- Improve code readability and maintainability

**Cons:**

- Additional classes increase codebase complexity
- May have overhead compared to primitive alternatives
- Require custom implementation in many languages
- Domain-specific, less general purpose
- Can be over-engineered for simple use cases

## Practice Problems

- **Meeting Rooms**: Use Interval class for overlap detection
- **Closest Pair of Points**: Point2D with distance calculations
- **LRU Cache with Expiration**: TTLCache implementation
- **Min Stack**: MinMaxStack for O(1) minimum queries
- **Top K Frequent Elements**: FrequencyCounter for efficient tracking
- **Coordinate-based Problems**: Pair class for grid representations

<details>
<summary>Implementation Notes (Advanced)</summary>

### Design Principles

- **Immutability**: Make data classes immutable when possible (like Point2D, Interval)
- **Value semantics**: Implement proper equals/hashCode for use in collections
- **Type safety**: Use generics appropriately for reusable components
- **Builder pattern**: For complex objects with many optional parameters

### Performance Considerations

- **Memory overhead**: Custom classes have object overhead vs primitives
- **Autoboxing**: Be aware of boxing costs with generic types
- **Garbage collection**: Frequent object creation can impact GC
- **Cache locality**: Consider struct-of-arrays vs array-of-structs patterns

### Integration with Standard Library

- **Comparable**: Implement for natural ordering in sorted collections
- **Serializable**: Add for persistence requirements
- **Cloneable**: Implement if deep copying is needed
- **Iterator**: Provide for custom collection types

### Common Patterns

- **Factory methods**: Static creation methods for common cases
- **Fluent interfaces**: Method chaining for complex operations
- **Visitor pattern**: For operations on heterogeneous structures
- **Strategy pattern**: For pluggable algorithms on data structures

### Testing Strategies

- **Edge cases**: Test boundary conditions for ranges/intervals
- **Equality contracts**: Verify equals/hashCode consistency
- **Invariants**: Test data structure invariants are maintained
- **Performance**: Benchmark against alternative implementations

### Memory and Performance Optimization

- **Object pooling**: Reuse objects for high-frequency operations
- **Primitive specialization**: Use primitive collections when appropriate
- **Lazy initialization**: Defer expensive computations until needed
- **Copy-on-write**: For immutable collections with frequent reads

</details>
