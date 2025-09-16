# Graph Adjacency Map

## Quick Definition

Graph representation using nested maps where each vertex maps to a collection of its neighbors. Provides flexible storage for sparse graphs with efficient neighbor lookups and edge weight storage.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add Vertex | **O(1)** | O(V + E) |
| Add Edge | **O(1)** | — |
| Remove Edge | **O(1)** | — |
| Get Neighbors | **O(1)** | — |
| Has Edge | **O(1)** | — |

*V = vertices, E = edges*

## Core Operations

```java
class GraphAdjacencyMap<T> {
    private Map<T, Map<T, Integer>> adjacencyMap; // vertex -> (neighbor -> weight)
    private boolean isDirected;
    
    public GraphAdjacencyMap(boolean isDirected) {
        this.adjacencyMap = new HashMap<>();
        this.isDirected = isDirected;
    }
    
    // Add a vertex to the graph
    public void addVertex(T vertex) {
        adjacencyMap.putIfAbsent(vertex, new HashMap<>());
    }
    
    // Add an edge between two vertices
    public void addEdge(T from, T to, int weight) {
        addVertex(from);
        addVertex(to);
        
        adjacencyMap.get(from).put(to, weight);
        
        if (!isDirected) {
            adjacencyMap.get(to).put(from, weight);
        }
    }
    
    // Check if edge exists
    public boolean hasEdge(T from, T to) {
        return adjacencyMap.containsKey(from) && 
               adjacencyMap.get(from).containsKey(to);
    }
    
    // Get all neighbors of a vertex
    public Set<T> getNeighbors(T vertex) {
        return adjacencyMap.getOrDefault(vertex, new HashMap<>()).keySet();
    }
    
    // BFS traversal
    public List<T> bfs(T start) {
        List<T> result = new ArrayList<>();
        Set<T> visited = new HashSet<>();
        Queue<T> queue = new LinkedList<>();
        
        queue.offer(start);
        visited.add(start);
        
        while (!queue.isEmpty()) {
            T vertex = queue.poll();
            result.add(vertex);
            
            for (T neighbor : getNeighbors(vertex)) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }
        return result;
    }
    
    // Find shortest path using BFS (unweighted)
    public List<T> shortestPath(T start, T end) {
        Map<T, T> parent = new HashMap<>();
        Set<T> visited = new HashSet<>();
        Queue<T> queue = new LinkedList<>();
        
        queue.offer(start);
        visited.add(start);
        parent.put(start, null);
        
        while (!queue.isEmpty()) {
            T current = queue.poll();
            
            if (current.equals(end)) {
                List<T> path = new ArrayList<>();
                T vertex = end;
                while (vertex != null) {
                    path.add(0, vertex);
                    vertex = parent.get(vertex);
                }
                return path;
            }
            
            for (T neighbor : getNeighbors(current)) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    parent.put(neighbor, current);
                    queue.offer(neighbor);
                }
            }
        }
        return new ArrayList<>();
    }
}

// Usage example
GraphAdjacencyMap<String> graph = new GraphAdjacencyMap<>(false);

// Build a social network graph
graph.addEdge("Alice", "Bob", 1);
graph.addEdge("Alice", "Charlie", 1);
graph.addEdge("Bob", "David", 1);
graph.addEdge("Charlie", "Eve", 1);

System.out.println("BFS from Alice: " + graph.bfs("Alice"));
System.out.println("Path Alice -> Eve: " + graph.shortestPath("Alice", "Eve"));

// Compare with simple Map<String, List<String>>
Map<String, List<String>> simpleGraph = new HashMap<>();
simpleGraph.put("Alice", Arrays.asList("Bob", "Charlie"));
simpleGraph.put("Bob", Arrays.asList("Alice", "David"));
```

## Python Snippet

```python
from collections import defaultdict, deque

class GraphAdjacencyMap:
    def __init__(self, directed=False):
        self.g = defaultdict(dict)   # u -> {v: weight}
        self.directed = directed
    def add_vertex(self, v):
        _ = self.g[v]
    def add_edge(self, u, v, w=1):
        self.add_vertex(u); self.add_vertex(v)
        self.g[u][v] = w
        if not self.directed:
            self.g[v][u] = w
    def has_edge(self, u, v):
        return v in self.g.get(u, {})
    def neighbors(self, u):
        return list(self.g.get(u, {}).keys())
    def bfs(self, start):
        seen, q, out = {start}, deque([start]), []
        while q:
            u = q.popleft(); out.append(u)
            for v in self.g.get(u, {}):
                if v not in seen:
                    seen.add(v); q.append(v)
        return out
    def shortest_path(self, s, t):  # unweighted
        parent, seen = {s: None}, {s}
        q = deque([s])
        while q:
            u = q.popleft()
            if u == t:
                path = []
                while u is not None:
                    path.append(u); u = parent[u]
                return path[::-1]
            for v in self.g.get(u, {}):
                if v not in seen:
                    seen.add(v); parent[v] = u; q.append(v)
        return []

# Usage
g = GraphAdjacencyMap(directed=False)
g.add_edge("Alice", "Bob"); g.add_edge("Alice", "Charlie"); g.add_edge("Bob", "David")
```

## When to Use

- Sparse graphs with few edges relative to vertices
- Weighted graphs requiring edge weight storage
- Dynamic graphs with frequent edge additions/removals
- Graphs with non-integer or complex edge data
- Social networks and relationship modeling

## Trade-offs

**Pros:**

- Efficient for sparse graphs
- Fast neighbor lookup O(1)
- Natural support for weighted edges
- Easy to add/remove edges dynamically
- Flexible vertex types

**Cons:**

- Higher memory overhead than adjacency lists
- Slower for dense graphs
- Hash map overhead for small graphs
- More complex than simple adjacency lists
- Not cache-friendly for large graphs

## Practice Problems

- **Clone Graph**: Deep copy using adjacency map
- **Course Schedule**: Topological sort with adjacency map
- **Network Delay Time**: Dijkstra's shortest path
- **Number of Islands**: Connected components
- **Shortest Path in Binary Matrix**: BFS on grid-based graph

<details>
<summary>Implementation Notes (Advanced)</summary>

### Data Structure Choice

- **HashMap vs TreeMap**: HashMap for O(1) access, TreeMap for sorted neighbors
- **HashSet vs ArrayList**: HashSet for neighbors prevents duplicates
- **Memory overhead**: Each map entry has overhead, consider for small graphs
- **Generic types**: Support for different vertex and edge weight types

### Performance Optimization

- **Load factor**: Tune HashMap load factor for performance
- **Initial capacity**: Size maps appropriately to avoid rehashing
- **Memory pooling**: Reuse map objects for frequent graph updates
- **Cache locality**: Consider adjacency list for better cache performance

### Algorithm Implementation

- **BFS/DFS**: Natural with adjacency map structure
- **Shortest path**: Dijkstra's algorithm with priority queue
- **Cycle detection**: DFS-based for undirected/directed graphs
- **Topological sort**: Kahn's algorithm or DFS-based

### Comparison with Alternatives

- **vs Adjacency List**: Map is more flexible, list is more memory efficient
- **vs Adjacency Matrix**: Map better for sparse graphs, matrix for dense
- **vs Edge List**: Map provides faster neighbor queries
- **Memory usage**: Higher overhead but more functionality

</details>
