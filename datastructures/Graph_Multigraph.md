# Graph Multigraph

## Quick Definition

A multigraph allows multiple edges between the same pair of vertices, supporting parallel edges with different weights or properties. Essential for modeling transportation networks, communication channels, and multi-relationship data where simple graphs are insufficient.

## Big-O Summary

| Operation | Average | Worst | Space |
|-----------|---------|-------|-------|
| Add Edge | O(1) | O(1) | O(E) |
| Remove Edge | O(k) | O(k) | O(1) |
| Find Edge | O(k) | O(k) | O(1) |
| Get All Edges | O(k) | O(k) | O(k) |
| BFS/DFS | O(V + E) | O(V + E) | O(V) |

*k = number of parallel edges between two vertices, E = total edges, V = vertices

## Core Operations

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.Collections;

// Edge class to represent weighted edges with optional labels
class MultiEdge {
    int to;
    double weight;
    String label;  // Optional edge type/label
    
    public MultiEdge(int to, double weight, String label) {
        this.to = to;
        this.weight = weight;
        this.label = label;
    }
    
    public MultiEdge(int to, double weight) {
        this(to, weight, null);
    }
    
    @Override
    public String toString() {
        return String.format("Edge(to=%d, weight=%.1f, label=%s)", to, weight, label);
    }
}

// Multigraph implementation using adjacency list with multiple edges
class Multigraph {
    private Map<Integer, List<MultiEdge>> adjList;
    private boolean directed;
    
    public Multigraph(boolean directed) {
        this.adjList = new HashMap<>();
        this.directed = directed;
    }
    
    // Add vertex if not exists
    public void addVertex(int vertex) {
        adjList.putIfAbsent(vertex, new ArrayList<>());
    }
    
    // Add edge (allows multiple edges between same vertices)
    public void addEdge(int from, int to, double weight, String label) {
        addVertex(from);
        addVertex(to);
        adjList.get(from).add(new MultiEdge(to, weight, label));
        if (!directed) {
            adjList.get(to).add(new MultiEdge(from, weight, label));
        }
    }
    
    public void addEdge(int from, int to, double weight) {
        addEdge(from, to, weight, null);
    }
    
    // Get all edges from a vertex
    public List<MultiEdge> getEdges(int vertex) {
        return adjList.getOrDefault(vertex, Collections.emptyList());
    }
    
    // Get all edges between two specific vertices
    public List<MultiEdge> getEdgesBetween(int from, int to) {
        List<MultiEdge> result = new ArrayList<>();
        for (MultiEdge edge : getEdges(from)) {
            if (edge.to == to) {
                result.add(edge);
            }
        }
        return result;
    }
    
    // Remove specific edge (removes first matching edge)
    public boolean removeEdge(int from, int to, double weight) {
        List<MultiEdge> edges = adjList.get(from);
        if (edges != null) {
            for (int i = 0; i < edges.size(); i++) {
                MultiEdge edge = edges.get(i);
                if (edge.to == to && Math.abs(edge.weight - weight) < 1e-9) {
                    edges.remove(i);
                    if (!directed) {
                        removeEdgeOneWay(to, from, weight);
                    }
                    return true;
                }
            }
        }
        return false;
    }
    
    private boolean removeEdgeOneWay(int from, int to, double weight) {
        List<MultiEdge> edges = adjList.get(from);
        if (edges != null) {
            for (int i = 0; i < edges.size(); i++) {
                MultiEdge edge = edges.get(i);
                if (edge.to == to && Math.abs(edge.weight - weight) < 1e-9) {
                    edges.remove(i);
                    return true;
                }
            }
        }
        return false;
    }
    
    // Count edges between two vertices
    public int getEdgeCount(int from, int to) {
        return getEdgesBetween(from, to).size();
    }
    
    // Get minimum weight edge between two vertices
    public Double getMinWeight(int from, int to) {
        return getEdgesBetween(from, to).stream()
                .mapToDouble(edge -> edge.weight)
                .min()
                .orElse(Double.NaN);
    }
    
    // Get all unique neighbors (regardless of parallel edges)
    public Set<Integer> getNeighbors(int vertex) {
        Set<Integer> neighbors = new HashSet<>();
        for (MultiEdge edge : getEdges(vertex)) {
            neighbors.add(edge.to);
        }
        return neighbors;
    }
    
    // Get total degree (counting parallel edges)
    public int getTotalDegree(int vertex) {
        return getEdges(vertex).size();
    }
    
    // Get unique degree (counting each neighbor once)
    public int getUniqueDegree(int vertex) {
        return getNeighbors(vertex).size();
    }
}

// Transportation network example
class TransportationNetwork extends Multigraph {
    public TransportationNetwork() {
        super(false); // undirected
    }
    
    public void addRoute(int city1, int city2, double distance, String transportType) {
        addEdge(city1, city2, distance, transportType);
    }
    
    public List<MultiEdge> getTransportOptions(int from, int to) {
        return getEdgesBetween(from, to);
    }
    
    public double getShortestRoute(int from, int to) {
        return getMinWeight(from, to);
    }
}

// Usage examples
Multigraph mg = new Multigraph(false);

// Multiple connections between cities (different transport types)
mg.addEdge(0, 1, 100.0, "highway");
mg.addEdge(0, 1, 150.0, "scenic_route");
mg.addEdge(0, 1, 80.0, "express");
mg.addEdge(1, 2, 200.0, "highway");

System.out.println("All edges from 0: " + mg.getEdges(0));
System.out.println("Edges between 0 and 1: " + mg.getEdgesBetween(0, 1));
System.out.println("Edge count 0->1: " + mg.getEdgeCount(0, 1)); // 3
System.out.println("Min weight 0->1: " + mg.getMinWeight(0, 1)); // 80.0
System.out.println("Unique neighbors of 0: " + mg.getNeighbors(0)); // [1]
System.out.println("Total degree of 0: " + mg.getTotalDegree(0)); // 6 (3 edges * 2 directions)

// Transportation network example
TransportationNetwork network = new TransportationNetwork();
network.addRoute(0, 1, 50, "bus");
network.addRoute(0, 1, 45, "train");
network.addRoute(0, 1, 30, "metro");

System.out.println("Transport options 0->1: " + network.getTransportOptions(0, 1));
System.out.println("Shortest route 0->1: " + network.getShortestRoute(0, 1)); // 30.0
```

## Python Snippet

```python
from collections import defaultdict

class MultiEdge:
    def __init__(self, to, weight, label=None):
        self.to, self.weight, self.label = to, weight, label
    def __repr__(self):
        return f"Edge(to={self.to}, weight={self.weight}, label={self.label})"

class Multigraph:
    def __init__(self, directed=False):
        self.g = defaultdict(list)
        self.directed = directed
    def add_edge(self, u, v, w, label=None):
        self.g[u].append(MultiEdge(v, w, label))
        if not self.directed:
            self.g[v].append(MultiEdge(u, w, label))
    def edges(self, u):
        return list(self.g.get(u, []))
    def edges_between(self, u, v):
        return [e for e in self.g.get(u, []) if e.to == v]
    def min_weight(self, u, v):
        es = self.edges_between(u, v)
        return min((e.weight for e in es), default=float('nan'))
    def neighbors(self, u):
        return {e.to for e in self.g.get(u, [])}

# Example
mg = Multigraph(False)
mg.add_edge(0, 1, 100.0, "highway")
mg.add_edge(0, 1, 150.0, "scenic_route")
mg.add_edge(0, 1, 80.0, "express")
```

## When to Use

- Transportation networks with multiple routes
- Communication networks with parallel channels
- Social networks with different relationship types
- Financial networks with multiple transaction types
- Any scenario requiring parallel edges with different properties

## Trade-offs

**Pros:**

- Supports parallel edges between vertices
- Can model complex real-world relationships
- Flexible edge labeling and properties
- Maintains all edge information
- Natural for multi-modal networks

**Cons:**

- Higher memory overhead than simple graphs
- More complex algorithms for some operations
- Edge queries can be O(k) where k is number of parallel edges
- Increased complexity for graph algorithms
- May need specialized algorithms for some problems

## Practice Problems

- **Shortest Path with Multiple Routes**: Modified Dijkstra's considering all parallel edges
- **Maximum Flow with Parallel Pipes**: Network flow with capacity on parallel edges
- **Multi-Modal Transportation**: Finding optimal routes across different transport types
- **Network Redundancy**: Analyzing connectivity with parallel communication channels
- **Currency Exchange**: Multiple exchange rates between currency pairs

<details>
<summary>Implementation Notes (Advanced)</summary>

### Edge Storage Strategies

- **List of edges**: Most flexible, allows any number of parallel edges
- **Map of lists**: `Map<Pair<Integer,Integer>, List<Edge>>` for direct edge access
- **Labeled edges**: Include edge types/labels for different relationships
- **Edge IDs**: Assign unique IDs to edges for direct reference

### Memory Optimization

- **Edge pooling**: Reuse edge objects to reduce garbage collection
- **Primitive collections**: Use specialized collections for better performance
- **Compression**: Store similar edges compactly
- **Lazy evaluation**: Create edge lists only when needed

### Algorithm Adaptations

- **BFS/DFS**: Typically treat parallel edges as single edges for traversal
- **Shortest path**: Consider all parallel edges to find minimum weight
- **Maximum flow**: Sum capacities of parallel edges
- **Minimum spanning tree**: Choose best edge among parallel options

### Parallel Edge Handling

- **Aggregation**: Sum, min, max, or average parallel edge weights
- **Selection**: Choose specific edge by criteria (weight, type, etc.)
- **Enumeration**: Iterate through all parallel edges
- **Filtering**: Select subset of edges based on properties

### Performance Considerations

- **Edge queries**: O(k) time where k is number of parallel edges
- **Memory usage**: Scales with total number of edges including parallel ones
- **Graph algorithms**: May need modification to handle parallel edges correctly
- **Serialization**: Consider efficient storage of parallel edge data

</details>
