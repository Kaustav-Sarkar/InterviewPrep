# Fenwick Tree (Binary Indexed Tree)

## Quick Definition

Array-based tree structure supporting efficient prefix sum queries and point updates. Uses binary representation to achieve O(log n) operations with simple implementation.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Update | **O(log n)** | O(n) |
| Prefix Sum | **O(log n)** | — |
| Range Sum | **O(log n)** | — |
| Build | O(n log n) | — |

## Core Operations

```java
class FenwickTree {
    private int[] tree;
    private int n;
    
    public FenwickTree(int size) {
        n = size;
        tree = new int[n + 1];  // 1-indexed for easier bit operations
    }
    
    public FenwickTree(int[] arr) {
        n = arr.length;
        tree = new int[n + 1];
        for (int i = 0; i < n; i++) {
            update(i, arr[i]);
        }
    }
    
    // Add delta to position i (0-indexed)
    public void update(int i, int delta) {
        i++;  // convert to 1-indexed
        while (i <= n) {
            tree[i] += delta;
            i += i & (-i);  // add lowest set bit
        }
    }
    
    // Get prefix sum [0, i] (inclusive, 0-indexed)
    public int prefixSum(int i) {
        i++;  // convert to 1-indexed
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= i & (-i);  // remove lowest set bit
        }
        return sum;
    }
    
    // Get range sum [left, right] (inclusive, 0-indexed)
    public int rangeSum(int left, int right) {
        return prefixSum(right) - (left > 0 ? prefixSum(left - 1) : 0);
    }
    
    // Set value at position i (not add)
    public void set(int i, int value) {
        int currentValue = rangeSum(i, i);
        update(i, value - currentValue);
    }
}

// 2D Fenwick Tree for matrix range sums
class FenwickTree2D {
    private int[][] tree;
    private int rows, cols;
    
    public FenwickTree2D(int rows, int cols) {
        this.rows = rows; this.cols = cols;
        tree = new int[rows + 1][cols + 1];
    }
    
    public void update(int r, int c, int delta) {
        for (int i = r + 1; i <= rows; i += i & (-i)) {
            for (int j = c + 1; j <= cols; j += j & (-j)) {
                tree[i][j] += delta;
            }
        }
    }
    
    public int prefixSum(int r, int c) {
        int sum = 0;
        for (int i = r + 1; i > 0; i -= i & (-i)) {
            for (int j = c + 1; j > 0; j -= j & (-j)) {
                sum += tree[i][j];
            }
        }
        return sum;
    }
    
    public int rangeSum(int r1, int c1, int r2, int c2) {
        return prefixSum(r2, c2) - prefixSum(r1 - 1, c2) 
               - prefixSum(r2, c1 - 1) + prefixSum(r1 - 1, c1 - 1);
    }
}

// Usage examples
FenwickTree ft = new FenwickTree(new int[]{1, 3, 5, 7, 9, 11});
System.out.println(ft.rangeSum(1, 3));  // sum of elements 1-3: 3+5+7 = 15
ft.update(2, 2);                        // add 2 to index 2: [1,3,7,7,9,11]
System.out.println(ft.rangeSum(1, 3));  // new sum: 3+7+7 = 17

// Counting inversions using Fenwick Tree
int countInversions(int[] arr) {
    int n = arr.length;
    
    // Coordinate compression
    Integer[] sorted = Arrays.stream(arr).boxed().toArray(Integer[]::new);
    Arrays.sort(sorted);
    Map<Integer, Integer> compress = new HashMap<>();
    for (int i = 0; i < n; i++) {
        compress.put(sorted[i], i);
    }
    
    FenwickTree ft = new FenwickTree(n);
    int inversions = 0;
    
    for (int i = n - 1; i >= 0; i--) {
        int compressed = compress.get(arr[i]);
        inversions += ft.prefixSum(compressed - 1);  // count smaller elements to the right
        ft.update(compressed, 1);
    }
    
    return inversions;
}

// Range update with lazy propagation (difference array)
class FenwickTreeRangeUpdate {
    private FenwickTree ft;
    
    public FenwickTreeRangeUpdate(int size) {
        ft = new FenwickTree(size);
    }
    
    // Add delta to range [left, right]
    public void rangeUpdate(int left, int right, int delta) {
        ft.update(left, delta);
        if (right + 1 < ft.n) ft.update(right + 1, -delta);
    }
    
    // Get value at position i
    public int pointQuery(int i) {
        return ft.prefixSum(i);
    }
}
```

## Python Snippet

```python
class FenwickTree:
    def __init__(self, n_or_arr):
        if isinstance(n_or_arr, int):
            self.n = n_or_arr
            self.t = [0]*(self.n+1)
        else:
            arr = n_or_arr
            self.n = len(arr)
            self.t = [0]*(self.n+1)
            for i, v in enumerate(arr):
                self.update(i, v)
    def update(self, i, delta):
        i += 1
        while i <= self.n:
            self.t[i] += delta
            i += i & -i
    def prefix_sum(self, i):
        i += 1; s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s
    def range_sum(self, l, r):
        return self.prefix_sum(r) - (self.prefix_sum(l-1) if l > 0 else 0)

# 2D Fenwick Tree
class Fenwick2D:
    def __init__(self, rows, cols):
        self.R, self.C = rows, cols
        self.t = [[0]*(cols+1) for _ in range(rows+1)]
    def update(self, r, c, delta):
        i = r + 1
        while i <= self.R:
            j = c + 1
            while j <= self.C:
                self.t[i][j] += delta
                j += j & -j
            i += i & -i
    def prefix_sum(self, r, c):
        s = 0; i = r + 1
        while i > 0:
            j = c + 1
            while j > 0:
                s += self.t[i][j]
                j -= j & -j
            i -= i & -i
        return s
    def range_sum(self, r1, c1, r2, c2):
        return (self.prefix_sum(r2, c2) - self.prefix_sum(r1-1, c2)
                - self.prefix_sum(r2, c1-1) + self.prefix_sum(r1-1, c1-1))
```

## When to Use

- Dynamic range sum queries with point updates
- Counting inversions in arrays
- Order statistics problems
- Coordinate compression with frequency counting
- 2D matrix range sum queries

## Trade-offs

**Pros:**

- Simple implementation compared to segment trees
- Lower memory overhead than segment trees
- Cache-friendly array-based structure
- Elegant bit manipulation operations

**Cons:**

- Limited to associative operations (sum, XOR, etc.)
- No range updates without additional techniques
- Less flexible than segment trees
- 1-indexed internal representation can be confusing

## Practice Problems

- **Range Sum Query - Mutable**: Dynamic array range sum queries
- **Count of Smaller Numbers After Self**: Inversions using coordinate compression
- **Range Addition**: Use difference array technique
- **Matrix Block Sum**: 2D Fenwick tree application
- **Reverse Pairs**: Count inversions with condition

<details>
<summary>Implementation Notes (Advanced)</summary>

### Bit Manipulation Explanation

- **Lowest set bit**: `i & (-i)` isolates rightmost 1-bit
- **Add operation**: Move to next position that this index contributes to
- **Query operation**: Move to parent that contains this index's contribution
- **Tree structure**: Implicit binary tree based on bit patterns

### Memory Layout

- **1-indexed**: Simplifies bit operations (avoids special case for index 0)
- **Array-based**: Better cache locality than pointer-based trees
- **Sparse updates**: Only O(log n) positions affected per update

### Extensions and Variants

- **Range updates**: Use difference array or dual Fenwick trees
- **2D/3D versions**: Nested bit operations for multi-dimensional queries
- **Order statistics**: Find kth smallest with coordinate compression
- **Max/Min queries**: Possible but segment tree usually preferred

### Performance Characteristics

- **Constants**: Lower constants than segment trees
- **Memory**: ~1/2 memory of equivalent segment tree
- **Implementation**: ~10 lines vs 50+ for segment tree
- **Flexibility**: Less flexible for complex operations

</details>
