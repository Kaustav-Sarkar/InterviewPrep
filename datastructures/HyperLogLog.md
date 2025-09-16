### Hyper Log Log

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
- Native: [Python](../python/native/hyper_log_log.py), [Java](../java/native/HyperLogLog.java)
- Std-lib–based: [Python](../python/stdlib/hyper_log_log_std.py), [Java](../java/stdlib/HyperLogLogStd.java)

#### Practice scenarios & interview-style questions
- Fast membership test with limited memory (Bloom).
- Approximate distinct count in streams (HLL).
- Heavy hitters / frequency estimation (CMS).
- Duplicate suppression in pipelines.
- Spam filtering / URL cache pre-check.

#### Further reading
- See curated notes in `../docs/`.
