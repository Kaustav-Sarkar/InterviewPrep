# Graph Adjacency Set

## Quick Definition

A graph representation where each vertex maps to a set of its neighbors, providing O(1) edge existence checking and automatic duplicate edge prevention. Ideal for unweighted graphs requiring frequent edge queries.

## Big-O Summary

| Operation | Average | Worst | Space |
|-----------|---------|-------|-------|
| Add Vertex | O(1) | O(1) | O(V + E) |
| Add Edge | O(1) | O(n) | O(1) |
| Remove Edge | O(1) | O(n) | O(1) |
| Has Edge | O(1) | O(n) | O(1) |
| Get Neighbors | O(degree) | O(degree) | O(1) |
| BFS/DFS | O(V + E) | O(V + E) | O(V) |

*n = number of neighbors of a vertex

## Core Operations

```java
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.TreeSet;
import java.util.Set;
import java.util.Map;
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

// Basic Graph using Set-based adjacency
class GraphAdjSet {
    private Map<Integer, Set<Integer>> adjSet;
    
    public GraphAdjSet() {
        this.adjSet = new HashMap<>();
    }
    
    public void addVertex(int v) {
        adjSet.putIfAbsent(v, new HashSet<>());
    }
    
    public void addEdge(int u, int v) {
        addVertex(u); addVertex(v);
        adjSet.get(u).add(v);
        adjSet.get(v).add(u); // undirected
    }
    
    public boolean hasEdge(int u, int v) {
        return adjSet.containsKey(u) && adjSet.get(u).contains(v);
    }
    
    public void removeEdge(int u, int v) {
        if (adjSet.containsKey(u)) adjSet.get(u).remove(v);
        if (adjSet.containsKey(v)) adjSet.get(v).remove(u);
    }
    
    public Set<Integer> getNeighbors(int v) {
        return adjSet.getOrDefault(v, Collections.emptySet());
    }
}

// Directed graph with Set-based adjacency
class DirectedGraphSet {
    private Map<Integer, Set<Integer>> outgoing = new HashMap<>();
    private Map<Integer, Set<Integer>> incoming = new HashMap<>();
    
    public void addEdge(int from, int to) {
        outgoing.putIfAbsent(from, new HashSet<>());
        incoming.putIfAbsent(to, new HashSet<>());
        outgoing.get(from).add(to);
        incoming.get(to).add(from);
    }
    
    public Set<Integer> getOutNeighbors(int v) {
        return outgoing.getOrDefault(v, Collections.emptySet());
    }
    
    public Set<Integer> getInNeighbors(int v) {
        return incoming.getOrDefault(v, Collections.emptySet());
    }
}

// Usage examples
GraphAdjSet graph = new GraphAdjSet();
graph.addEdge(1, 2); graph.addEdge(2, 3); graph.addEdge(3, 4);
System.out.println("Has edge 1-2: " + graph.hasEdge(1, 2)); // true
System.out.println("Neighbors of 2: " + graph.getNeighbors(2)); // [1, 3]

// BFS traversal using set-based adjacency
public List<Integer> bfsTraversal(GraphAdjSet graph, int start) {
    List<Integer> result = new ArrayList<>();
    Set<Integer> visited = new HashSet<>();
    Queue<Integer> queue = new ArrayDeque<>();
    
    queue.add(start);
    visited.add(start);
    
    while (!queue.isEmpty()) {
        int current = queue.poll();
        result.add(current);
        
        for (int neighbor : graph.getNeighbors(current)) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                queue.add(neighbor);
            }
        }
    }
    return result;
}

// String-based adjacency set (social networks)
Map<String, Set<String>> friendsGraph = new HashMap<>();
friendsGraph.put("Alice", new HashSet<>(Arrays.asList("Bob", "Charlie")));
friendsGraph.put("Bob", new HashSet<>(Arrays.asList("Alice", "David")));
System.out.println("Alice's friends: " + friendsGraph.get("Alice"));
```

## Python Snippet

```python
from collections import defaultdict, deque

class GraphAdjSet:
    def __init__(self, directed=False):
        self.out = defaultdict(set)
        self.directed = directed
    def add_edge(self, u, v):
        self.out[u].add(v)
        if not self.directed:
            self.out[v].add(u)
    def has_edge(self, u, v):
        return v in self.out.get(u, set())
    def neighbors(self, u):
        return self.out.get(u, set())
    def bfs(self, s):
        seen, q, order = {s}, deque([s]), []
        while q:
            u = q.popleft(); order.append(u)
            for v in self.out.get(u, set()):
                if v not in seen:
                    seen.add(v); q.append(v)
        return order
```

## When to Use

- Unweighted graphs with frequent edge existence queries
- Graphs requiring duplicate edge prevention
- Social networks and friendship graphs
- Bidirectional relationships without weights
- Graph algorithms that need fast edge lookup

## Trade-offs

**Pros:**

- O(1) edge existence checking
- Automatic duplicate edge prevention
- Clean API for graph operations
- Efficient for sparse graphs
- Set operations (intersection, union) on neighbors

**Cons:**

- Higher memory overhead than adjacency lists
- Cannot store edge weights directly
- Set iteration order not guaranteed (unless TreeSet)
- Slower neighbor iteration than lists
- Hash set overhead for small neighborhoods

## Practice Problems

- **Number of Connected Components**: Union-Find or DFS traversal
- **Graph Valid Tree**: Check if graph is connected and acyclic
- **Course Schedule**: Cycle detection in directed graph
- **Clone Graph**: Deep copy with set-based adjacency
- **Find if Path Exists**: BFS/DFS between two nodes

<details>
<summary>Implementation Notes (Advanced)</summary>

### Set Implementation Choice

- **HashSet**: O(1) operations, unordered neighbors
- **LinkedHashSet**: O(1) operations, insertion order preserved
- **TreeSet**: O(log n) operations, sorted neighbors
- **Memory overhead**: Set objects have higher overhead than lists

### Performance Characteristics

- **Edge queries**: Constant time with hash sets
- **Neighbor iteration**: Slightly slower than lists due to set overhead
- **Memory usage**: Higher than adjacency lists, lower than adjacency matrix for sparse graphs
- **Cache performance**: Hash sets can have poor cache locality

### Common Optimizations

- **Initial capacity**: Size sets appropriately for known graph density
- **Load factor**: Tune HashSet load factor for performance
- **Primitive sets**: Use TIntHashSet for integer vertices to reduce boxing
- **Bidirectional edges**: Consider storing only one direction to save memory

### Algorithm Considerations

- **BFS/DFS**: Natural implementation with set-based adjacency
- **Cycle detection**: Efficient edge existence checking
- **Graph coloring**: Fast neighbor queries for conflict checking
- **Set operations**: Natural union/intersection on neighbor sets

</details>
