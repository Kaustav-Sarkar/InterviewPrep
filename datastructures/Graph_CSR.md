### Graph C S R

#### Definition & core idea
Concise definition and the intuition behind the structure.

#### Time–space complexity
| Operation | Average | Worst | Space |
|---|---|---|---|
| Insert | TBD | TBD | TBD |
| Delete | TBD | TBD | TBD |
| Search/Access | TBD | TBD | TBD |

#### Real-world use-cases
- Add concrete scenarios where this excels (systems, apps, infra).

#### When to choose over alternatives
- Guidance on trade-offs vs. neighboring structures.

#### Implementations
- Native: [Python](../python/native/graph_c_s_r.py), [Java](../java/native/GraphCSR.java)
- Std-lib–based: [Python](../python/stdlib/graph_c_s_r_std.py), [Java](../java/stdlib/GraphCSRStd.java)

#### Practice scenarios & interview-style questions
- Find shortest path in an unweighted graph (BFS on adjacency list).
- Detect cycles in a directed graph (DFS, recursion stack).
- Topological sort for task scheduling (Kahn/DFS).
- Check if a graph is bipartite (BFS coloring).
- Count connected components in an undirected graph.
- Design adjacency representation for sparse vs dense graphs (CSR vs matrix).
- Implement Dijkstra on adjacency list with a min-heap.
- Model a grid as a graph to solve shortest path with obstacles.
- Track parallel edges/self-loops in a multigraph.
- Store weighted graphs with map-of-maps (AdjacencyMap).

#### Further reading
- See curated notes in `../docs/`.
