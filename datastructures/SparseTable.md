# Sparse Table

## Quick Definition

Static data structure for answering range queries on immutable arrays in O(1) time after O(n log n) preprocessing. Optimal for idempotent operations like min/max.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n log n) | O(n log n) |
| Range Query | **O(1)** | — |
| Update | Not supported | — |
| Space | — | O(n log n) |

## Core Operations

```java
// Range Minimum Query (RMQ) Sparse Table
class SparseTableRMQ {
    private int[][] st;
    private int[] log;
    private int n;
    
    public SparseTableRMQ(int[] arr) {
        n = arr.length;
        int maxLog = (int) (Math.log(n) / Math.log(2)) + 1;
        st = new int[n][maxLog];
        log = new int[n + 1];
        
        // Precompute logarithms
        log[1] = 0;
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        // Initialize first column
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }
        
        // Build sparse table using DP
        for (int j = 1; (1 << j) <= n; j++) {
            for (int i = 0; i + (1 << j) - 1 < n; i++) {
                st[i][j] = Math.min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    // Range minimum query [left, right] (inclusive)
    public int query(int left, int right) {
        int k = log[right - left + 1];
        return Math.min(st[left][k], st[right - (1 << k) + 1][k]);
    }
}

// Range Maximum Query (RMQ) Sparse Table
class SparseTableRMX {
    private int[][] st;
    private int[] log;
    private int n;
    
    public SparseTableRMX(int[] arr) {
        n = arr.length;
        int maxLog = (int) (Math.log(n) / Math.log(2)) + 1;
        st = new int[n][maxLog];
        log = new int[n + 1];
        
        // Precompute logarithms
        log[1] = 0;
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        // Initialize first column
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }
        
        // Build sparse table
        for (int j = 1; (1 << j) <= n; j++) {
            for (int i = 0; i + (1 << j) - 1 < n; i++) {
                st[i][j] = Math.max(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    public int query(int left, int right) {
        int k = log[right - left + 1];
        return Math.max(st[left][k], st[right - (1 << k) + 1][k]);
    }
}

// Generic Sparse Table for any idempotent operation
class GenericSparseTable<T> {
    private T[][] st;
    private int[] log;
    private int n;
    private BinaryOperator<T> combiner;
    
    @SuppressWarnings("unchecked")
    public GenericSparseTable(T[] arr, BinaryOperator<T> combiner) {
        this.n = arr.length;
        this.combiner = combiner;
        int maxLog = (int) (Math.log(n) / Math.log(2)) + 1;
        
        st = (T[][]) new Object[n][maxLog];
        log = new int[n + 1];
        
        // Precompute logarithms
        log[1] = 0;
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        // Initialize first column
        for (int i = 0; i < n; i++) {
            st[i][0] = arr[i];
        }
        
        // Build sparse table
        for (int j = 1; (1 << j) <= n; j++) {
            for (int i = 0; i + (1 << j) - 1 < n; i++) {
                st[i][j] = combiner.apply(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    public T query(int left, int right) {
        int k = log[right - left + 1];
        return combiner.apply(st[left][k], st[right - (1 << k) + 1][k]);
    }
}

// 2D Sparse Table for 2D range queries
class SparseTable2D {
    private int[][][][] st;
    private int[] log;
    private int rows, cols;
    
    public SparseTable2D(int[][] matrix) {
        rows = matrix.length;
        cols = matrix[0].length;
        int logR = (int) (Math.log(rows) / Math.log(2)) + 1;
        int logC = (int) (Math.log(cols) / Math.log(2)) + 1;
        
        st = new int[rows][cols][logR][logC];
        log = new int[Math.max(rows, cols) + 1];
        
        // Precompute logarithms
        log[1] = 0;
        for (int i = 2; i < log.length; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        // Initialize base case
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                st[i][j][0][0] = matrix[i][j];
            }
        }
        
        // Build sparse table
        for (int ki = 0; (1 << ki) <= rows; ki++) {
            for (int kj = 0; (1 << kj) <= cols; kj++) {
                if (ki == 0 && kj == 0) continue;
                for (int i = 0; i + (1 << ki) - 1 < rows; i++) {
                    for (int j = 0; j + (1 << kj) - 1 < cols; j++) {
                        if (ki == 0) {
                            st[i][j][ki][kj] = Math.min(
                                st[i][j][ki][kj - 1],
                                st[i][j + (1 << (kj - 1))][ki][kj - 1]
                            );
                        } else {
                            st[i][j][ki][kj] = Math.min(
                                st[i][j][ki - 1][kj],
                                st[i + (1 << (ki - 1))][j][ki - 1][kj]
                            );
                        }
                    }
                }
            }
        }
    }
    
    public int query(int r1, int c1, int r2, int c2) {
        int ki = log[r2 - r1 + 1];
        int kj = log[c2 - c1 + 1];
        
        return Math.min(
            Math.min(st[r1][c1][ki][kj], st[r2 - (1 << ki) + 1][c1][ki][kj]),
            Math.min(st[r1][c2 - (1 << kj) + 1][ki][kj], st[r2 - (1 << ki) + 1][c2 - (1 << kj) + 1][ki][kj])
        );
    }
}

// Usage examples
int[] arr = {7, 2, 3, 0, 5, 10, 3, 12, 18};
SparseTableRMQ st = new SparseTableRMQ(arr);

System.out.println(st.query(1, 3)); // minimum in range [1,3]: 0
System.out.println(st.query(4, 6)); // minimum in range [4,6]: 3

// Generic usage
Integer[] intArr = {7, 2, 3, 0, 5, 10, 3, 12, 18};
GenericSparseTable<Integer> gst = new GenericSparseTable<>(intArr, Integer::min);
System.out.println(gst.query(1, 3)); // 0
```

## Python Snippet

```python
import math

class SparseTableMin:
    def __init__(self, arr):
        self.n = len(arr)
        self.log = [0]*(self.n+1)
        for i in range(2, self.n+1): self.log[i] = self.log[i//2] + 1
        K = self.log[self.n] + 1
        self.st = [[0]*K for _ in range(self.n)]
        for i in range(self.n): self.st[i][0] = arr[i]
        j = 1
        while (1<<j) <= self.n:
            i = 0
            while i + (1<<j) - 1 < self.n:
                self.st[i][j] = min(self.st[i][j-1], self.st[i + (1<<(j-1))][j-1])
                i += 1
            j += 1
    def query(self, L, R):
        k = self.log[R-L+1]
        return min(self.st[L][k], self.st[R-(1<<k)+1][k])
```

## When to Use

- Static arrays requiring frequent range minimum/maximum queries
- Preprocessing phase acceptable for faster query times
- Range GCD, LCM queries (idempotent operations)
- 2D matrix range queries for minimum/maximum
- Online algorithms with no updates to underlying data

## Trade-offs

**Pros:**

- O(1) query time after preprocessing
- Perfect for static range queries
- Works for any idempotent operation
- Extends to higher dimensions

**Cons:**

- O(n log n) space complexity
- No support for updates
- Only works for idempotent operations
- High preprocessing time

## Practice Problems

- **Range Minimum Query**: Classic sparse table application
- **Range Maximum Query**: Similar to RMQ but with max operation
- **Range GCD Query**: Use sparse table for GCD queries
- **2D Range Sum**: Though typically use 2D prefix sums
- **Longest Common Prefix**: Build sparse table on suffix array

<details>
<summary>Implementation Notes (Advanced)</summary>

### Idempotent Operations

- **Definition**: f(x, x) = x for all x
- **Examples**: min, max, gcd, lcm, bitwise AND/OR
- **Non-examples**: sum, product (require different approach)
- **Query overlap**: Idempotent property allows overlapping ranges

### Space Optimization

- **Row reduction**: Some implementations use less space
- **Lazy computation**: Build only needed ranges
- **Memory layout**: Consider cache-friendly access patterns

### Extensions

- **Higher dimensions**: 3D, 4D sparse tables possible
- **Different operations**: Custom comparators for objects
- **Range types**: Adapt for different query ranges

### Comparison with Alternatives

- **vs Segment Tree**: No updates but faster queries
- **vs Square Root Decomposition**: Better query time, worse space
- **vs Binary Lifting**: Similar technique, different applications

</details>
