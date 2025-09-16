# Binomial Heap

## Quick Definition

Collection of binomial trees that supports mergeable heap operations efficiently. Each binomial tree satisfies heap property and has a specific structure enabling fast merging.

## Big-O Summary

| Operation | Time (Amortized) | Space |
|-----------|------------------|-------|
| Insert | **O(1)** | O(n) |
| Find Min | **O(log n)** | — |
| Extract Min | **O(log n)** | — |
| Merge | **O(log n)** | — |
| Decrease Key | **O(log n)** | — |

## Core Operations

```java
class BinomialNode {
    int key;
    int degree;
    BinomialNode parent, child, sibling;
    
    public BinomialNode(int key) {
        this.key = key;
        this.degree = 0;
    }
}

class BinomialHeap {
    private BinomialNode head; // head of root list
    
    public void insert(int key) {
        BinomialHeap newHeap = new BinomialHeap();
        newHeap.head = new BinomialNode(key);
        this.merge(newHeap);
    }
    
    public int findMin() {
        BinomialNode minNode = head;
        BinomialNode current = head.sibling;
        
        while (current != null) {
            if (current.key < minNode.key) {
                minNode = current;
            }
            current = current.sibling;
        }
        return minNode.key;
    }
    
    public int extractMin() {
        // Find and remove minimum node
        // Create heap from children
        // Merge with remaining heap
        // ... implementation details
        return 0; // placeholder
    }
    
    public void merge(BinomialHeap other) {
        this.head = mergeRootLists(this.head, other.head);
        consolidate();
    }
}

// Usage with Java PriorityQueue comparison
BinomialHeap bheap = new BinomialHeap();
PriorityQueue<Integer> pq = new PriorityQueue<>();

// Both support similar operations
bheap.insert(10); pq.offer(10);
bheap.insert(5);  pq.offer(5);

System.out.println("Binomial min: " + bheap.findMin()); // 5
System.out.println("PriorityQueue min: " + pq.peek()); // 5

// Binomial heap excels at merging
BinomialHeap other = new BinomialHeap();
other.insert(3);
bheap.merge(other); // O(log n) merge
```

## Python Snippet

```python
class BinNode:
    __slots__ = ('key','deg','parent','child','sibling')
    def __init__(self, key):
        self.key=key; self.deg=0; self.parent=self.child=self.sibling=None

def _link(y, z):
    y.parent = z; y.sibling = z.child; z.child = y; z.deg += 1

def _merge_roots(a, b):
    head = tail = None
    while a and b:
        x = a if a.deg <= b.deg else b
        if x is a: a = a.sibling
        else: b = b.sibling
        if not head: head = tail = x
        else: tail.sibling = x; tail = x
    rest = a or b
    if not head: return rest
    tail.sibling = rest; return head

class BinomialHeap:
    def __init__(self): self.head = None
    def merge(self, other):
        self.head = _merge_roots(self.head, other.head)
        if not self.head: return
        prev = None; curr = self.head; nxt = curr.sibling
        while nxt:
            if curr.deg != nxt.deg or (nxt.sibling and nxt.sibling.deg == curr.deg):
                prev, curr, nxt = curr, nxt, nxt.sibling
            elif curr.key <= nxt.key:
                curr.sibling = nxt.sibling; _link(nxt, curr); nxt = curr.sibling
            else:
                if prev: prev.sibling = nxt
                else: self.head = nxt
                _link(curr, nxt); curr = nxt; nxt = curr.sibling
    def insert(self, key):
        h = BinomialHeap(); h.head = BinNode(key); self.merge(h)
    def find_min(self):
        x = self.head; best = None; val = float('inf')
        while x:
            if x.key < val: val = x.key; best = x
            x = x.sibling
        return val if best is not None else None
```

## When to Use

- Mergeable priority queues in distributed systems
- Graph algorithms requiring decrease-key operations
- Parallel processing with multiple priority queues
- Advanced algorithms like Dijkstra's with decrease-key
- Applications requiring frequent heap merging

## Trade-offs

**Pros:**

- Efficient merging O(log n)
- Good amortized insert time O(1)
- Supports decrease-key operation
- Flexible structure for parallel algorithms
- Better than binary heaps for merging

**Cons:**

- Complex implementation
- Higher constant factors than binary heaps
- More memory overhead per node
- Worse cache performance than array-based heaps
- Rarely needed in practice

## Practice Problems

- **Merge k Sorted Lists**: Use mergeable heaps efficiently
- **Network Delay Time**: Dijkstra's with decrease-key
- **Parallel Priority Queues**: Merge distributed priority queues
- **Task Scheduling**: Merge priority queues from different processors
- **Minimum Spanning Tree**: Prim's algorithm with decrease-key

<details>
<summary>Implementation Notes (Advanced)</summary>

### Binomial Tree Properties

- **Recursive structure**: Binomial tree B_k has 2^k nodes
- **Degree sequence**: Root list contains trees of distinct degrees
- **Height**: Binomial tree B_k has height k
- **Structure**: B_k formed by linking two B_(k-1) trees

### Merge Algorithm

- **Root list merging**: Merge sorted by degree
- **Consolidation**: Combine trees of same degree
- **Linking**: Smaller root becomes parent
- **Complexity**: O(log n) due to at most log n trees

### Decrease Key Operation

- **Bubble up**: Move decreased key toward root
- **Cut operation**: If heap property violated, cut subtree
- **Cascading cuts**: Propagate cuts up the tree
- **Amortized analysis**: O(log n) amortized time

### Comparison with Alternatives

- **vs Binary Heap**: Better for merging, worse for simple operations
- **vs Fibonacci Heap**: Simpler but worse decrease-key performance
- **vs Pairing Heap**: Simpler implementation, similar performance
- **Memory usage**: Higher overhead than array-based heaps

</details>
