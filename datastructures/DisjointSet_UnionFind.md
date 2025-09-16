# Disjoint Set (Union-Find)

## Quick Definition

Data structure that tracks disjoint sets and supports efficient union and find operations. Uses path compression and union by rank for near-constant time complexity.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Find | **O(α(n))** | O(n) |
| Union | **O(α(n))** | — |
| Connected | **O(α(n))** | — |
| Count Sets | **O(1)** | — |
*α(n) = inverse Ackermann function (practically constant)*

## Core Operations

```java
class UnionFind {
    private int[] parent;
    private int[] rank;      // tree height for union by rank
    private int components;  // number of disjoint sets
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        components = n;
        
        // Initially each element is its own parent
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 0;
        }
    }
    
    // Find with path compression
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);  // path compression
        }
        return parent[x];
    }
    
    // Union by rank
    public boolean union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return false;  // already connected
        
        // Union by rank: attach smaller tree under larger tree
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        
        components--;
        return true;
    }
    
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }
    
    public int getComponents() {
        return components;
    }
    
    // Get size of component containing x
    public int getSize(int x) {
        Map<Integer, Integer> sizes = new HashMap<>();
        for (int i = 0; i < parent.length; i++) {
            int root = find(i);
            sizes.put(root, sizes.getOrDefault(root, 0) + 1);
        }
        return sizes.get(find(x));
    }
}

// Advanced version with size tracking
class WeightedUnionFind {
    private int[] parent;
    private int[] size;      // size of component for union by size
    private int components;
    
    public WeightedUnionFind(int n) {
        parent = new int[n];
        size = new int[n];
        components = n;
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }
    
    public int find(int x) {
        int root = x;
        while (parent[root] != root) root = parent[root];
        
        // Path compression: point all nodes on path to root
        while (parent[x] != x) {
            int next = parent[x];
            parent[x] = root;
            x = next;
        }
        return root;
    }
    
    public boolean union(int x, int y) {
        int rootX = find(x), rootY = find(y);
        if (rootX == rootY) return false;
        
        // Union by size: attach smaller tree to larger
        if (size[rootX] < size[rootY]) {
            parent[rootX] = rootY;
            size[rootY] += size[rootX];
        } else {
            parent[rootY] = rootX;
            size[rootX] += size[rootY];
        }
        
        components--;
        return true;
    }
    
    public int getComponentSize(int x) {
        return size[find(x)];
    }
}

// Usage examples
UnionFind uf = new UnionFind(5);  // elements 0,1,2,3,4
uf.union(0, 1);  // connect 0 and 1
uf.union(2, 3);  // connect 2 and 3
boolean connected = uf.connected(0, 1);  // true
int components = uf.getComponents();     // 3 components: {0,1}, {2,3}, {4}

// Grid percolation example
boolean percolates(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    UnionFind uf = new UnionFind(m * n + 2);  // +2 for virtual top/bottom
    int top = m * n, bottom = m * n + 1;
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 1) {
                int current = i * n + j;
                
                // Connect to virtual top/bottom
                if (i == 0) uf.union(current, top);
                if (i == m - 1) uf.union(current, bottom);
                
                // Connect to adjacent open cells
                int[][] dirs = {{-1,0}, {1,0}, {0,-1}, {0,1}};
                for (int[] dir : dirs) {
                    int ni = i + dir[0], nj = j + dir[1];
                    if (ni >= 0 && ni < m && nj >= 0 && nj < n && grid[ni][nj] == 1) {
                        uf.union(current, ni * n + nj);
                    }
                }
            }
        }
    }
    
    return uf.connected(top, bottom);
}
```

## Python Snippet

```python
class UnionFind:
    def __init__(self, n):
        self.p = list(range(n)); self.r = [0]*n; self.components = n
    def find(self, x):
        if self.p[x] != x: self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.r[ra] < self.r[rb]: ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]: self.r[ra] += 1
        self.components -= 1; return True
    def connected(self, a, b):
        return self.find(a) == self.find(b)
```

## When to Use

- Dynamic connectivity queries in graphs
- Kruskal's minimum spanning tree algorithm
- Cycle detection in undirected graphs
- Percolation problems and grid connectivity
- Account merging and equivalence relations

## Trade-offs

**Pros:**

- Near-constant time operations with optimizations
- Simple to implement and understand
- Excellent for dynamic connectivity problems
- Memory-efficient O(n) space

**Cons:**

- No efficient way to split/disconnect components
- Only supports union operations, not deletions
- Path compression makes structure immutable for some applications
- Not suitable for range queries or complex relationships

## Practice Problems

- **Number of Connected Components**: Count components in undirected graph
- **Redundant Connection**: Find edge that creates cycle
- **Accounts Merge**: Group accounts by common email addresses
- **Friend Circles**: Count groups of mutual friends
- **Satisfiability of Equality Equations**: Check consistency of equality constraints

<details>
<summary>Implementation Notes (Advanced)</summary>

### Optimization Techniques

- **Path compression**: Make every node point directly to root
- **Union by rank**: Attach shorter tree to taller tree
- **Union by size**: Attach smaller tree to larger tree
- **Path halving**: Make every node point to grandparent

### Time Complexity Analysis

- **Without optimizations**: O(n) per operation in worst case
- **With path compression only**: O(log n) amortized
- **With union by rank only**: O(log n) per operation
- **With both optimizations**: O(α(n)) where α is inverse Ackermann

### Space Considerations

- **Rank array**: Can be eliminated in some implementations
- **Size tracking**: Useful for component size queries
- **Memory layout**: Arrays provide better cache locality than trees

### Variants and Extensions

- **Weighted Union-Find**: Track distances/relationships
- **Persistent Union-Find**: Support rollback operations
- **Online/Offline**: Static vs dynamic connectivity problems
- **Link-Cut Trees**: More general but complex alternative

</details>
