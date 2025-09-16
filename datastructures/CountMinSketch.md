### Count Min Sketch

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
- Native: [Python](../python/native/count_min_sketch.py), [Java](../java/native/CountMinSketch.java)
- Std-lib–based: [Python](../python/stdlib/count_min_sketch_std.py), [Java](../java/stdlib/CountMinSketchStd.java)

#### Practice scenarios & interview-style questions
- Fast membership test with limited memory (Bloom).
- Approximate distinct count in streams (HLL).
- Heavy hitters / frequency estimation (CMS).
- Duplicate suppression in pipelines.
- Spam filtering / URL cache pre-check.

#### Further reading
- See curated notes in `../docs/`.
