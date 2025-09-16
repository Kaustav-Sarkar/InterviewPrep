# Segment Tree

## Quick Definition

Complete binary tree supporting efficient range queries and updates. Each node represents an interval and stores aggregate information (sum, min, max) for that range.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(4n) |
| Range Query | **O(log n)** | — |
| Point Update | **O(log n)** | — |
| Range Update | O(log n) | — |

## Core Operations

```java
class SegmentTree {
    private int[] tree;
    private int n;
    
    public SegmentTree(int[] arr) {
        n = arr.length;
        tree = new int[4 * n];  // safe upper bound
        build(arr, 1, 0, n - 1);
    }
    
    // Build tree recursively
    private void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1];  // sum query
        }
    }
    
    // Range sum query [l, r]
    public int query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }
    
    private int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;  // no overlap
        if (l <= start && end <= r) return tree[node];  // complete overlap
        
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) + 
               query(2 * node + 1, mid + 1, end, l, r);
    }
    
    // Point update: set arr[idx] = val
    public void update(int idx, int val) {
        update(1, 0, n - 1, idx, val);
    }
    
    private void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) {
                update(2 * node, start, mid, idx, val);
            } else {
                update(2 * node + 1, mid + 1, end, idx, val);
            }
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }
    }
}

// Range Minimum Query (RMQ) Segment Tree
class RMQSegmentTree {
    private int[] tree;
    private int n;
    
    public RMQSegmentTree(int[] arr) {
        n = arr.length;
        tree = new int[4 * n];
        build(arr, 1, 0, n - 1);
    }
    
    private void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
        }
    }
    
    public int rangeMin(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }
    
    private int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return Integer.MAX_VALUE;
        if (l <= start && end <= r) return tree[node];
        
        int mid = (start + end) / 2;
        return Math.min(query(2 * node, start, mid, l, r),
                       query(2 * node + 1, mid + 1, end, l, r));
    }
}

// Generic Segment Tree with custom operations
class GenericSegmentTree<T> {
    private T[] tree;
    private int n;
    private BinaryOperator<T> combine;
    private T identity;
    
    @SuppressWarnings("unchecked")
    public GenericSegmentTree(T[] arr, BinaryOperator<T> combineOp, T identityVal) {
        n = arr.length;
        tree = (T[]) new Object[4 * n];
        combine = combineOp;
        identity = identityVal;
        build(arr, 1, 0, n - 1);
    }
    
    // Usage examples
    public static void main(String[] args) {
        // Sum segment tree
        Integer[] arr = {1, 3, 5, 7, 9, 11};
        GenericSegmentTree<Integer> sumTree = new GenericSegmentTree<>(arr, Integer::sum, 0);
        
        // Min segment tree
        GenericSegmentTree<Integer> minTree = new GenericSegmentTree<>(arr, Integer::min, Integer.MAX_VALUE);
        
        // Max segment tree
        GenericSegmentTree<Integer> maxTree = new GenericSegmentTree<>(arr, Integer::max, Integer.MIN_VALUE);
    }
}

// Count of elements in range [a, b] using coordinate compression
class CountSegmentTree {
    private SegmentTree st;
    private Map<Integer, Integer> compressed;
    
    public CountSegmentTree(int[] values) {
        // Coordinate compression
        Integer[] sorted = Arrays.stream(values).boxed().distinct().sorted().toArray(Integer[]::new);
        compressed = new HashMap<>();
        for (int i = 0; i < sorted.length; i++) {
            compressed.put(sorted[i], i);
        }
        
        st = new SegmentTree(new int[sorted.length]);
    }
    
    public void add(int value) {
        int compressed_idx = compressed.get(value);
        int current = st.query(compressed_idx, compressed_idx);
        st.update(compressed_idx, current + 1);
    }
    
    public int countInRange(int a, int b) {
        int left = compressed.getOrDefault(a, 0);
        int right = compressed.getOrDefault(b, compressed.size() - 1);
        return st.query(left, right);
    }
}
```

## Python Snippet

```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0]*(4*self.n)
        self._build(arr, 1, 0, self.n-1)
    def _build(self, a, v, l, r):
        if l == r:
            self.t[v] = a[l]
        else:
            m = (l+r)//2
            self._build(a, v*2, l, m)
            self._build(a, v*2+1, m+1, r)
            self.t[v] = self.t[v*2] + self.t[v*2+1]
    def query(self, L, R):
        return self._query(1, 0, self.n-1, L, R)
    def _query(self, v, l, r, L, R):
        if R < l or r < L: return 0
        if L <= l and r <= R: return self.t[v]
        m = (l+r)//2
        return self._query(v*2, l, m, L, R) + self._query(v*2+1, m+1, r, L, R)
    def update(self, idx, val):
        self._update(1, 0, self.n-1, idx, val)
    def _update(self, v, l, r, idx, val):
        if l == r: self.t[v] = val
        else:
            m = (l+r)//2
            if idx <= m: self._update(v*2, l, m, idx, val)
            else: self._update(v*2+1, m+1, r, idx, val)
            self.t[v] = self.t[v*2] + self.t[v*2+1]

# RMQ variant
class RMQSegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0]*(4*self.n)
        self._build(arr, 1, 0, self.n-1)
    def _build(self, a, v, l, r):
        if l == r: self.t[v] = a[l]
        else:
            m = (l+r)//2
            self._build(a, v*2, l, m)
            self._build(a, v*2+1, m+1, r)
            self.t[v] = min(self.t[v*2], self.t[v*2+1])
    def range_min(self, L, R):
        return self._q(1, 0, self.n-1, L, R)
    def _q(self, v, l, r, L, R):
        if R < l or r < L: return float('inf')
        if L <= l and r <= R: return self.t[v]
        m = (l+r)//2
        return min(self._q(v*2, l, m, L, R), self._q(v*2+1, m+1, r, L, R))
```

## When to Use

- Dynamic range sum/min/max queries
- Range updates with lazy propagation
- Online algorithms requiring range operations
- Competitive programming problems
- Real-time analytics on sliding windows

## Trade-offs

**Pros:**

- Supports range queries and updates in O(log n)
- More flexible than Fenwick trees
- Can handle any associative operation
- Supports range updates with lazy propagation

**Cons:**

- Higher memory overhead (4n space)
- More complex implementation than Fenwick tree
- Higher constant factors
- Recursive calls can cause stack overflow

## Practice Problems

- **Range Sum Query - Mutable**: Basic segment tree application
- **Range Minimum Query**: RMQ using segment tree
- **Count of Range Sum**: Coordinate compression + segment tree
- **Range Addition**: Lazy propagation segment tree
- **Falling Squares**: Coordinate compression with max segment tree

<details>
<summary>Implementation Notes (Advanced)</summary>

### Tree Structure

- **Complete binary tree**: Stored in array with index-based navigation
- **Node indexing**: Left child = 2*i, right child = 2*i+1
- **Memory allocation**: 4n is safe upper bound for array size
- **1-indexed**: Often easier for node navigation

### Range Query Patterns

- **No overlap**: Query range doesn't intersect node range
- **Complete overlap**: Node range completely inside query range
- **Partial overlap**: Recursively query children

### Lazy Propagation

- **Range updates**: Update entire ranges in O(log n)
- **Delayed propagation**: Push updates down only when needed
- **Update types**: Add, assign, multiply operations

### Memory and Performance

- **Space complexity**: O(4n) for tree array
- **Cache locality**: Better than pointer-based trees
- **Iterative implementation**: Can avoid recursion overhead
- **Bottom-up construction**: Alternative building approach

</details>
