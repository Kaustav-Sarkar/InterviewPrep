# Segment Tree with Lazy Propagation

## Quick Definition

Enhanced segment tree that defers range updates using lazy propagation, enabling efficient range updates and queries. Updates are propagated down the tree only when necessary.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Range Query | **O(log n)** | O(n) |
| Range Update | **O(log n)** | — |
| Point Query | **O(log n)** | — |
| Point Update | **O(log n)** | — |

## Core Operations

```java
class LazySegmentTree {
    private long[] tree;   // segment tree values
    private long[] lazy;   // lazy propagation values
    private int[] arr;     // original array
    private int n;         // size of original array

    public LazySegmentTree(int[] nums) {
        this.arr = nums;
        this.n = nums.length;
        this.tree = new long[4 * n];
        this.lazy = new long[4 * n];
        build(0, 0, n - 1);
    }

    // Build the segment tree
    private void build(int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(2 * node + 1, start, mid);
            build(2 * node + 2, mid + 1, end);
            tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
        }
    }

    // Push lazy value down to children
    private void push(int node, int start, int end) {
        if (lazy[node] != 0) {
            tree[node] += lazy[node] * (end - start + 1);
            
            if (start != end) { // Not a leaf node
                lazy[2 * node + 1] += lazy[node];
                lazy[2 * node + 2] += lazy[node];
            }
            
            lazy[node] = 0;
        }
    }

    // Range update: add value to range [L, R]
    public void updateRange(int L, int R, int value) {
        updateRange(0, 0, n - 1, L, R, value);
    }

    // Range query: sum of range [L, R]
    public long queryRange(int L, int R) {
        return queryRange(0, 0, n - 1, L, R);
    }
}

// Usage examples
int[] nums = {1, 3, 5, 7, 9, 11};
LazySegmentTree lst = new LazySegmentTree(nums);

System.out.println("Initial sum [1, 4]: " + lst.queryRange(1, 4)); // 24
lst.updateRange(1, 3, 5); // Add 5 to range [1, 3]
System.out.println("After update: " + lst.queryRange(1, 4)); // 39
```

## Python Snippet

```python
class LazySegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0]*(4*self.n)
        self.lazy = [0]*(4*self.n)
        self._build(arr, 1, 0, self.n-1)
    def _build(self, a, v, l, r):
        if l == r: self.t[v] = a[l]
        else:
            m = (l+r)//2
            self._build(a, v*2, l, m)
            self._build(a, v*2+1, m+1, r)
            self.t[v] = self.t[v*2] + self.t[v*2+1]
    def _push(self, v, l, r):
        if self.lazy[v] != 0:
            self.t[v] += self.lazy[v] * (r - l + 1)
            if l != r:
                self.lazy[v*2] += self.lazy[v]
                self.lazy[v*2+1] += self.lazy[v]
            self.lazy[v] = 0
    def update_range(self, L, R, val):
        self._upd(1, 0, self.n-1, L, R, val)
    def _upd(self, v, l, r, L, R, val):
        self._push(v, l, r)
        if R < l or r < L: return
        if L <= l and r <= R:
            self.lazy[v] += val
            self._push(v, l, r)
            return
        m = (l+r)//2
        self._upd(v*2, l, m, L, R, val)
        self._upd(v*2+1, m+1, r, L, R, val)
        self.t[v] = self.t[v*2] + self.t[v*2+1]
    def query_range(self, L, R):
        return self._qry(1, 0, self.n-1, L, R)
    def _qry(self, v, l, r, L, R):
        self._push(v, l, r)
        if R < l or r < L: return 0
        if L <= l and r <= R: return self.t[v]
        m = (l+r)//2
        return self._qry(v*2, l, m, L, R) + self._qry(v*2+1, m+1, r, L, R)
```

## When to Use

- Range updates with range queries
- Competitive programming problems
- Array manipulation with bulk operations
- Time series data with interval modifications
- Game development for area effects

## Trade-offs

**Pros:**

- Efficient range updates O(log n)
- Handles both range and point operations
- Deferred computation saves time
- Supports various operations (sum, min, max, assignment)
- Better than naive O(n) range updates

**Cons:**

- More complex than basic segment tree
- Higher constant factors due to lazy propagation
- Requires careful implementation of push operations
- Memory overhead for lazy array
- Can be tricky to debug

## Practice Problems

- **Range Sum Query - Mutable**: With range updates
- **My Calendar III**: Booking conflicts with lazy propagation
- **Range Addition**: Multiple range increment operations
- **Falling Squares**: Heights with range maximum queries
- **Count of Range Sum**: Range sum counts in intervals

<details>
<summary>Implementation Notes (Advanced)</summary>

### Lazy Propagation Strategy

- **Deferred updates**: Store updates without immediate application
- **Push when needed**: Propagate only when accessing nodes
- **Update types**: Addition, assignment, multiplication
- **Composition**: Combine multiple pending updates

### Push Operation Design

- **Leaf handling**: Different logic for leaf vs internal nodes
- **Update propagation**: Pass lazy values to children
- **Tree maintenance**: Update current node values
- **Clearing flags**: Reset lazy values after propagation

### Range vs Point Operations

- **Range updates**: Efficient with lazy propagation
- **Point queries**: May require full path propagation
- **Mixed workloads**: Balance between range and point operations
- **Query optimization**: Minimize unnecessary propagation

### Advanced Techniques

- **Lazy with different operations**: Addition, assignment, multiplication
- **2D lazy propagation**: Extend to rectangle updates
- **Persistent lazy trees**: Maintain multiple versions
- **Parallel processing**: Concurrent access with proper synchronization

</details>
