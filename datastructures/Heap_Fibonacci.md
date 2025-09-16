# Fibonacci Heap

## Quick Definition

Advanced mergeable heap with excellent amortized performance for decrease-key operations. Uses lazy consolidation and cascading cuts to achieve optimal theoretical bounds.

## Big-O Summary

| Operation | Time (Amortized) | Space |
|-----------|------------------|-------|
| Insert | **O(1)** | O(n) |
| Find Min | **O(1)** | — |
| Extract Min | **O(log n)** | — |
| Merge | **O(1)** | — |
| Decrease Key | **O(1)** | — |

## Core Operations

```java
class FibonacciNode {
    int key;
    int degree;
    boolean marked;
    FibonacciNode parent, child, left, right;
    
    public FibonacciNode(int key) {
        this.key = key;
        this.degree = 0;
        this.marked = false;
        this.left = this.right = this;
    }
}

class FibonacciHeap {
    private FibonacciNode min;
    private int size;
    
    public FibonacciNode insert(int key) {
        FibonacciNode node = new FibonacciNode(key);
        if (min == null) {
            min = node;
        } else {
            addToRootList(node);
            if (node.key < min.key) {
                min = node;
            }
        }
        size++;
        return node;
    }
    
    public int findMin() {
        return min != null ? min.key : Integer.MAX_VALUE;
    }
    
    // O(1) amortized decrease key operation
    public void decreaseKey(FibonacciNode node, int newKey) {
        node.key = newKey;
        FibonacciNode parent = node.parent;
        
        if (parent != null && node.key < parent.key) {
            cut(node, parent);
            cascadingCut(parent);
        }
        
        if (node.key < min.key) {
            min = node;
        }
    }
    
    // O(1) merge operation
    public void merge(FibonacciHeap other) {
        // Concatenate root lists in O(1)
        // Update minimum pointer
        size += other.size;
    }
}

// Usage comparing with PriorityQueue
FibonacciHeap fheap = new FibonacciHeap();
PriorityQueue<Integer> pq = new PriorityQueue<>();

FibonacciNode node = fheap.insert(10);
pq.offer(10);

// Fibonacci heap supports O(1) decrease-key
fheap.decreaseKey(node, 5);

// PriorityQueue requires remove + re-insert for decrease-key
// which is O(n) operation
```

## Python Snippet

```python
class FibNode:
    def __init__(self, k):
        self.key=k; self.degree=0; self.mark=False
        self.parent=None; self.child=None; self.left=self; self.right=self

def _concat(a, b):
    if not a: return b
    if not b: return a
    a.right.left, b.left.right = b.left, a.right
    a.right, b.left = b, a
    return a

class FibonacciHeap:
    def __init__(self): self.min=None; self.n=0
    def insert(self, k):
        node = FibNode(k)
        self.min = _concat(self.min, node)
        if not self.min or node.key < self.min.key: self.min = node
        self.n += 1; return node
    def merge(self, other):
        self.min = _concat(self.min, other.min)
        if other.min and (not self.min or other.min.key < self.min.key): self.min = other.min
        self.n += other.n
    def find_min(self):
        return self.min.key if self.min else None
```

## When to Use

- Dijkstra's shortest path with decrease-key operations
- Prim's minimum spanning tree algorithm
- Network optimization algorithms
- Algorithms requiring frequent decrease-key operations
- Theoretical algorithm analysis

## Trade-offs

**Pros:**

- Excellent amortized bounds for decrease-key O(1)
- Fast merging O(1)
- Optimal for algorithms with many decrease-key operations
- Best theoretical performance for certain graph algorithms
- Lazy evaluation defers expensive operations

**Cons:**

- Very complex implementation
- High constant factors in practice
- Poor cache performance
- Large memory overhead
- Rarely faster than binary heaps in practice

## Practice Problems

- **Network Delay Time**: Dijkstra's algorithm implementation
- **Minimum Cost to Connect Sticks**: Priority queue operations
- **Cheapest Flights Within K Stops**: Modified Dijkstra's
- **Path with Maximum Probability**: Shortest path variant
- **Connecting Cities with Minimum Cost**: Minimum spanning tree

<details>
<summary>Implementation Notes (Advanced)</summary>

### Amortized Analysis

- **Potential function**: Based on number of trees and marked nodes
- **Decrease key**: O(1) amortized through cascading cuts
- **Extract min**: O(log n) amortized through consolidation
- **Insert and merge**: O(1) actual time

### Cascading Cuts

- **Mark propagation**: Cut marked nodes when they lose children
- **Bounded depth**: Limits tree height for good amortized bounds
- **Lazy evaluation**: Defers consolidation until extract-min
- **Balance maintenance**: Keeps trees relatively balanced

### Consolidation Process

- **Degree table**: Array indexed by tree degree
- **Tree linking**: Combine trees of same degree
- **Root list rebuild**: Maintain minimum pointer
- **Lazy approach**: Only consolidate during extract-min

### Practical Considerations

- **Implementation complexity**: Very difficult to implement correctly
- **Constant factors**: High overhead makes it slow in practice
- **Memory usage**: Significant pointer overhead
- **Cache performance**: Poor locality due to pointer structure
- **Alternative**: Pairing heaps often perform better in practice

</details>
