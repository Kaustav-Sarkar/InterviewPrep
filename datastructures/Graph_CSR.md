# Graph CSR (Compressed Sparse Row)

## Quick Definition

Compressed Sparse Row format stores a graph using three arrays: row pointers (where each row starts), column indices (neighbors), and values (edge weights). Provides efficient neighbor access O(degree) and excellent memory locality for graph algorithms.

## Big-O Summary

| Operation | Average | Worst | Space |
|-----------|---------|-------|-------|
| Build CSR | O(V + E) | O(V + E) | O(V + E) |
| Get Neighbors | O(degree) | O(degree) | O(1) |
| Find Edge | O(degree) | O(degree) | O(1) |
| BFS/DFS | O(V + E) | O(V + E) | O(V) |
| SpMV | O(V + E) | O(V + E) | O(V) |
| Matrix Ops | O(V + E) | O(V + E) | O(1) |

*V = vertices, E = edges, degree = out-degree of vertex

## Core Operations

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;

// CSR Graph implementation
class GraphCSR {
    private int[] rowPtr;      // Row pointers: rowPtr[i] = start of row i
    private int[] colIdx;      // Column indices (neighbors)
    private double[] values;   // Edge weights
    private int numVertices;
    private int numEdges;
    
    // Constructor from adjacency list
    public GraphCSR(Map<Integer, List<Integer>> adjList, int numVertices) {
        this.numVertices = numVertices;
        buildFromAdjList(adjList);
    }
    
    // Constructor from edge list (COO format)
    public GraphCSR(List<int[]> edges, int numVertices) {
        this.numVertices = numVertices;
        buildFromEdgeList(edges);
    }
    
    // Build CSR from adjacency list
    private void buildFromAdjList(Map<Integer, List<Integer>> adjList) {
        // Count edges and create arrays
        this.numEdges = adjList.values().stream().mapToInt(List::size).sum();
        this.rowPtr = new int[numVertices + 1];
        this.colIdx = new int[numEdges];
        this.values = new double[numEdges];
        
        int edgeIdx = 0;
        for (int i = 0; i < numVertices; i++) {
            rowPtr[i] = edgeIdx;
            List<Integer> neighbors = adjList.getOrDefault(i, Collections.emptyList());
            for (int neighbor : neighbors) {
                colIdx[edgeIdx] = neighbor;
                values[edgeIdx] = 1.0; // Default weight
                edgeIdx++;
            }
        }
        rowPtr[numVertices] = numEdges; // End marker
    }
    
    // Build CSR from edge list
    private void buildFromEdgeList(List<int[]> edges) {
        // Convert to adjacency list first, then build CSR
        Map<Integer, List<Integer>> adjList = new HashMap<>();
        for (int[] edge : edges) {
            int from = edge[0], to = edge[1];
            adjList.computeIfAbsent(from, k -> new ArrayList<>()).add(to);
        }
        buildFromAdjList(adjList);
    }
    
    // Get neighbors of a vertex (O(degree))
    public int[] getNeighbors(int vertex) {
        int start = rowPtr[vertex];
        int end = rowPtr[vertex + 1];
        return Arrays.copyOfRange(colIdx, start, end);
    }
    
    // Get edge weights for a vertex
    public double[] getEdgeWeights(int vertex) {
        int start = rowPtr[vertex];
        int end = rowPtr[vertex + 1];
        return Arrays.copyOfRange(values, start, end);
    }
    
    // Check if edge exists (O(degree))
    public boolean hasEdge(int from, int to) {
        int start = rowPtr[from];
        int end = rowPtr[from + 1];
        for (int i = start; i < end; i++) {
            if (colIdx[i] == to) return true;
        }
        return false;
    }
    
    // Get edge weight (O(degree))
    public Double getEdgeWeight(int from, int to) {
        int start = rowPtr[from];
        int end = rowPtr[from + 1];
        for (int i = start; i < end; i++) {
            if (colIdx[i] == to) return values[i];
        }
        return null;
    }
    
    // Get vertex degree
    public int getDegree(int vertex) {
        return rowPtr[vertex + 1] - rowPtr[vertex];
    }
    
    // Sparse Matrix-Vector multiplication: y = Ax
    public double[] matrixVectorMultiply(double[] x) {
        double[] y = new double[numVertices];
        for (int i = 0; i < numVertices; i++) {
            double sum = 0.0;
            for (int j = rowPtr[i]; j < rowPtr[i + 1]; j++) {
                sum += values[j] * x[colIdx[j]];
            }
            y[i] = sum;
        }
        return y;
    }
    
    // BFS traversal using CSR
    public List<Integer> bfs(int start) {
        boolean[] visited = new boolean[numVertices];
        List<Integer> result = new ArrayList<>();
        java.util.Queue<Integer> queue = new java.util.ArrayDeque<>();
        
        queue.add(start);
        visited[start] = true;
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            result.add(current);
            
            // Iterate through neighbors using CSR
            for (int i = rowPtr[current]; i < rowPtr[current + 1]; i++) {
                int neighbor = colIdx[i];
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
        return result;
    }
    
    // Getters for internal arrays (for debugging/analysis)
    public int[] getRowPtr() { return Arrays.copyOf(rowPtr, rowPtr.length); }
    public int[] getColIdx() { return Arrays.copyOf(colIdx, colIdx.length); }
    public double[] getValues() { return Arrays.copyOf(values, values.length); }
}

// Usage examples
Map<Integer, List<Integer>> adjList = new HashMap<>();
adjList.put(0, Arrays.asList(1, 2));
adjList.put(1, Arrays.asList(2, 3));
adjList.put(2, Arrays.asList(3));
adjList.put(3, Arrays.asList());

GraphCSR graph = new GraphCSR(adjList, 4);

System.out.println("Neighbors of 0: " + Arrays.toString(graph.getNeighbors(0))); // [1, 2]
System.out.println("Degree of 1: " + graph.getDegree(1)); // 2
System.out.println("Has edge 0->2: " + graph.hasEdge(0, 2)); // true
System.out.println("BFS from 0: " + graph.bfs(0)); // [0, 1, 2, 3]

// Sparse matrix-vector multiplication
double[] x = {1.0, 2.0, 3.0, 4.0};
double[] result = graph.matrixVectorMultiply(x);
System.out.println("SpMV result: " + Arrays.toString(result));
```

## Python Snippet

```python
# CSR arrays: row_ptr, col_idx, vals
class GraphCSR:
    def __init__(self, adj=None, n=None):
        if adj is not None:
            self._build_from_adj(adj, n if n is not None else (max(adj.keys())+1))
    def _build_from_adj(self, adj, n):
        self.n = n
        row_ptr = [0]*(n+1)
        col_idx = []
        vals = []
        cnt = 0
        for i in range(n):
            row_ptr[i] = cnt
            for v in adj.get(i, []):
                col_idx.append(v); vals.append(1.0); cnt += 1
        row_ptr[n] = cnt
        self.row_ptr, self.col_idx, self.vals = row_ptr, col_idx, vals
    def neighbors(self, u):
        i, j = self.row_ptr[u], self.row_ptr[u+1]
        return self.col_idx[i:j]
    def degree(self, u):
        return self.row_ptr[u+1] - self.row_ptr[u]
    def has_edge(self, u, v):
        i, j = self.row_ptr[u], self.row_ptr[u+1]
        return v in self.col_idx[i:j]
    def spmv(self, x):
        y = [0.0]*self.n
        for i in range(self.n):
            s = 0.0
            for k in range(self.row_ptr[i], self.row_ptr[i+1]):
                s += self.vals[k] * x[self.col_idx[k]]
            y[i] = s
        return y
```

## When to Use

- High-performance graph algorithms requiring many traversals
- Sparse matrix computations in scientific computing
- Graph neural networks and machine learning
- When memory locality and cache performance matter
- Read-heavy workloads with infrequent graph modifications

## Trade-offs

**Pros:**

- Excellent cache locality and memory efficiency
- Fast neighbor iteration O(degree)
- Optimal for read-heavy graph algorithms
- Compact representation for sparse graphs
- Industry standard for high-performance computing

**Cons:**

- Immutable structure - expensive to modify
- O(V + E) time to build from other formats
- Requires knowing total vertex count upfront
- No direct edge insertion/deletion
- More complex to implement than adjacency lists

## Practice Problems

- **PageRank Algorithm**: Iterative matrix-vector multiplications
- **Breadth-First Search**: Cache-efficient graph traversal
- **Shortest Path Algorithms**: Dijkstra's with priority queue
- **Graph Coloring**: Efficient neighbor access for conflict checking
- **Connected Components**: DFS/BFS with optimal memory access

<details>
<summary>Implementation Notes (Advanced)</summary>

### CSR Structure and Layout

- **Row pointers**: `rowPtr[i]` points to start of row i in column array
- **Column indices**: Sorted neighbors for each vertex (optional but recommended)
- **Values array**: Edge weights aligned with column indices
- **End marker**: `rowPtr[V]` contains total number of edges

### Construction Optimization

- **From COO**: Sort by row, then construct row pointers
- **From adjacency list**: Direct construction as shown in code
- **Sorting neighbors**: Improves cache performance and enables binary search
- **Memory allocation**: Pre-allocate arrays to avoid resizing

### Cache Optimization

- **Sequential access**: CSR optimized for row-wise iteration
- **Memory prefetching**: Hardware prefetchers work well with CSR
- **Data locality**: Neighbors stored contiguously in memory
- **False sharing**: Minimal in CSR due to sequential access patterns

### Matrix Operations

- **SpMV (Sparse Matrix-Vector)**: Core operation for many algorithms
- **SpMM (Sparse Matrix-Matrix)**: Can be implemented efficiently
- **Transpose**: Requires building CSC (Compressed Sparse Column) format
- **Matrix addition**: Efficient when both matrices in CSR format

### Performance Considerations

- **Branch prediction**: Minimize conditional branches in inner loops
- **SIMD optimization**: Vectorization possible for SpMV operations
- **Parallel processing**: Natural parallelization over rows
- **Memory bandwidth**: Often memory-bound due to sparse nature

</details>
