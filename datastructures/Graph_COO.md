# Graph COO (Coordinate Format)

## Quick Definition

COOrdinate format stores a graph as three parallel arrays: source vertices, destination vertices, and edge weights. Ideal for sparse graphs requiring efficient storage and matrix operations, commonly used in scientific computing and machine learning.

## Big-O Summary

| Operation | Average | Worst | Space |
|-----------|---------|-------|-------|
| Add Edge | O(1) | O(1) | O(E) |
| Find Edge | O(E) | O(E) | O(1) |
| Remove Edge | O(E) | O(E) | O(1) |
| Get Neighbors | O(E) | O(E) | O(degree) |
| BFS/DFS | O(E) per vertex | O(VE) | O(V) |
| Matrix Operations | O(E) | O(E) | O(E) |

*E = number of edges, V = number of vertices

## Core Operations

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;
import java.util.Collections;
import java.util.stream.IntStream;

// Basic COO format implementation
class GraphCOO {
    private List<Integer> rowIndices;    // source vertices
    private List<Integer> colIndices;    // destination vertices
    private List<Double> values;         // edge weights
    
    public GraphCOO() {
        this.rowIndices = new ArrayList<>();
        this.colIndices = new ArrayList<>();
        this.values = new ArrayList<>();
    }
    
    // Add weighted edge
    public void addEdge(int from, int to, double weight) {
        rowIndices.add(from);
        colIndices.add(to);
        values.add(weight);
    }
    
    // Add unweighted edge (weight = 1.0)
    public void addEdge(int from, int to) {
        addEdge(from, to, 1.0);
    }
    
    // Find edge weight (O(E) - linear search)
    public Double findEdge(int from, int to) {
        for (int i = 0; i < rowIndices.size(); i++) {
            if (rowIndices.get(i) == from && colIndices.get(i) == to) {
                return values.get(i);
            }
        }
        return null; // Edge not found
    }
    
    // Get all neighbors of a vertex
    public List<Integer> getNeighbors(int vertex) {
        List<Integer> neighbors = new ArrayList<>();
        for (int i = 0; i < rowIndices.size(); i++) {
            if (rowIndices.get(i) == vertex) {
                neighbors.add(colIndices.get(i));
            }
        }
        return neighbors;
    }
    
    // Get edge count
    public int getEdgeCount() {
        return rowIndices.size();
    }
    
    // Convert to adjacency matrix (dense representation)
    public double[][] toAdjacencyMatrix(int numVertices) {
        double[][] matrix = new double[numVertices][numVertices];
        for (int i = 0; i < rowIndices.size(); i++) {
            int row = rowIndices.get(i);
            int col = colIndices.get(i);
            double val = values.get(i);
            matrix[row][col] = val;
        }
        return matrix;
    }
    
    // Matrix-vector multiplication: Ax = b
    public double[] matrixVectorMultiply(double[] x, int numVertices) {
        double[] result = new double[numVertices];
        for (int i = 0; i < rowIndices.size(); i++) {
            int row = rowIndices.get(i);
            int col = colIndices.get(i);
            double val = values.get(i);
            result[row] += val * x[col];
        }
        return result;
    }
}

// Unweighted COO graph (simpler)
class UnweightedCOO {
    private int[] sources;
    private int[] targets;
    private int edgeCount;
    
    public UnweightedCOO(int maxEdges) {
        this.sources = new int[maxEdges];
        this.targets = new int[maxEdges];
        this.edgeCount = 0;
    }
    
    public void addEdge(int from, int to) {
        sources[edgeCount] = from;
        targets[edgeCount] = to;
        edgeCount++;
    }
    
    public boolean hasEdge(int from, int to) {
        for (int i = 0; i < edgeCount; i++) {
            if (sources[i] == from && targets[i] == to) {
                return true;
            }
        }
        return false;
    }
    
    public int[] getSources() { return Arrays.copyOf(sources, edgeCount); }
    public int[] getTargets() { return Arrays.copyOf(targets, edgeCount); }
    public int getEdgeCount() { return edgeCount; }
}

// Usage examples
GraphCOO graph = new GraphCOO();
graph.addEdge(0, 1, 2.5);
graph.addEdge(0, 2, 1.0);
graph.addEdge(1, 2, 3.0);
graph.addEdge(2, 0, 0.5);

System.out.println("Edge (0,1) weight: " + graph.findEdge(0, 1)); // 2.5
System.out.println("Neighbors of 0: " + graph.getNeighbors(0));   // [1, 2]

// Convert to dense matrix for algorithms requiring matrix operations
double[][] adjMatrix = graph.toAdjacencyMatrix(3);
System.out.println("Adjacency matrix: " + Arrays.deepToString(adjMatrix));

// Sparse matrix operations
double[] x = {1.0, 2.0, 3.0};
double[] result = graph.matrixVectorMultiply(x, 3);
System.out.println("Matrix-vector product: " + Arrays.toString(result));
```

## Python Snippet

```python
# COO triplet lists
class GraphCOO:
    def __init__(self):
        self.rows, self.cols, self.vals = [], [], []
    def add_edge(self, u, v, w=1.0):
        self.rows.append(u); self.cols.append(v); self.vals.append(w)
    def find_edge(self, u, v):
        for r, c, w in zip(self.rows, self.cols, self.vals):
            if r == u and c == v: return w
        return None
    def neighbors(self, u):
        return [c for r, c in zip(self.rows, self.cols) if r == u]
    def to_matrix(self, n):
        M = [[0.0]*n for _ in range(n)]
        for r, c, w in zip(self.rows, self.cols, self.vals):
            M[r][c] = w
        return M
    def spmv(self, x, n):  # y = A x
        y = [0.0]*n
        for r, c, w in zip(self.rows, self.cols, self.vals):
            y[r] += w * x[c]
        return y
```

## When to Use

- Sparse matrices and graphs in scientific computing
- Graph neural networks and machine learning applications
- Interoperability with matrix computation libraries
- Memory-efficient storage for very sparse graphs
- When parallel edge processing is needed

## Trade-offs

**Pros:**

- Extremely memory efficient for sparse graphs
- Simple triplet format (row, col, value)
- Excellent for matrix operations
- Easy to serialize and transfer
- Natural for parallel processing of edges

**Cons:**

- O(E) time for edge queries and neighbor lookup
- Inefficient for graph traversal algorithms
- No fast vertex degree computation
- Requires sorting for some optimizations
- Poor cache locality for graph algorithms

## Practice Problems

- **Sparse Matrix Multiplication**: COO format matrix operations
- **Graph Isomorphism**: Compare edge lists in COO format
- **Minimum Spanning Tree**: Sort edges by weight (Kruskal's)
- **Edge Betweenness Centrality**: Process all edges uniformly
- **Network Flow**: Convert to appropriate format for flow algorithms

<details>
<summary>Implementation Notes (Advanced)</summary>

### Memory Layout and Optimization

- **Parallel arrays**: Keep row/col/value arrays synchronized
- **Primitive arrays**: Use int[] and double[] instead of ArrayList for better performance
- **Memory alignment**: Consider struct-of-arrays vs array-of-structs
- **Compression**: Store as sorted triplets for better compression

### Conversion to Other Formats

- **To CSR**: Sort by row, then create row pointers
- **To adjacency matrix**: Direct indexing for dense conversion
- **To adjacency list**: Group by source vertex
- **From edge list**: Natural mapping to COO format

### Matrix Operations

- **SpMV (Sparse Matrix-Vector)**: Core operation for many algorithms
- **Matrix addition**: Element-wise operations on matching indices
- **Transpose**: Swap row and column indices
- **Sorting**: By row, then column for canonical form

### Performance Considerations

- **Sequential access**: COO is optimized for sequential edge processing
- **Random access**: Very poor performance for random edge queries
- **Memory usage**: Minimal overhead, 3 values per edge
- **Parallelization**: Embarrassingly parallel for many operations

</details>
