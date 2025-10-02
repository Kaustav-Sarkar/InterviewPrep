# CountMinSketch

## Quick Refresh
- Probabilistic structure to estimate frequency counts using sub-linear memory.
- Overestimates counts but never underestimates, making it safe for throttling decisions.
- Uses multiple hash functions to update a 2D matrix of counters; query takes the minimum across hashes.

## When to Reach For It
- Track request frequencies for rate limiting when the key space is huge.
- Detect heavy hitters in streaming data (top URLs, abusive IPs).
- Provide fast estimates for join cardinality in query planners.

## Example Scenario
API gateway throttling billions of requests/day:
- Each request increments counters for the associated API key across multiple hash buckets.
- When deciding if an API key exceeds its quota, the gateway reads the minimum counter value.
- Occasional overestimation keeps the system safe; real-time dashboards account for the margin.

## Visualization
```mermaid
graph LR
    Request[Incoming Key]
    Hash1[Hash h1]
    Hash2[Hash h2]
    Hash3[Hash h3]
    Matrix[Counter Matrix]

    Request --> Hash1 --> Matrix
    Request --> Hash2 --> Matrix
    Request --> Hash3 --> Matrix

    Query[Frequency Query] --> Hash1
    Query --> Hash2
    Query --> Hash3
    Hash1 --> Matrix
    Hash2 --> Matrix
    Hash3 --> Matrix
    Matrix --> Result[Min(h1,h2,h3)]
```

## Operational Guidance
- Configure width `w = ceil(e/ε)` and depth `d = ceil(ln(1/δ))` for error ε and confidence 1-δ.
- For high accuracy, use 4–5 hash functions and thousands of columns; measure actual error in staging.
- Conservative update variants limit counter inflation; use them when tight bounds are needed.
- Reset or age out counters for sliding time windows to prevent unbounded growth.

## Deepen Your Understanding
- Hello Interview – Probabilistic Structures: https://www.hellointerview.com/learn/system-design/probabilistic-data-structures
- Gaurav Sen – Count-Min Sketch: https://youtu.be/5hA9TAnxd1k
- ByteByteGo – Streaming Algorithms Overview: https://youtu.be/k9H6dXuJdJQ
