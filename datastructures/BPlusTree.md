### B+ Tree

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
- Native: [Python](../python/native/b_plus_tree.py), [Java](../java/native/BPlusTree.java)
- Std-lib–based: [Python](../python/stdlib/b_plus_tree_std.py), [Java](../java/stdlib/BPlusTreeStd.java)

#### Practice scenarios & interview-style questions
- Disk-friendly ordered index (DB storage engine).
- Range scans with minimal IO (B+ tree leaves).
- Implement key compression / high fan-out nodes.
- Multi-version concurrency (conceptual).
- Filesystem directory indexing.

#### Further reading
- See curated notes in `../docs/`.
