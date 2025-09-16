# Count-Min Sketch

## Quick Definition

Probabilistic data structure for frequency estimation in data streams using multiple hash functions and a 2D array. Provides approximate counts with guaranteed error bounds.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Update | **O(k)** | O(k × w) |
| Query | **O(k)** | — |
| Memory | — | O(1/ε × log δ⁻¹) |

*k = number of hash functions, w = width, ε = error rate, δ = failure probability*

## Core Operations

```java
class CountMinSketch {
    private int[][] sketch;
    private int width, depth;
    private int[] hashA, hashB;
    private static final int LARGE_PRIME = 982451653;
    
    public CountMinSketch(double epsilon, double delta) {
        this.width = (int) Math.ceil(Math.E / epsilon);
        this.depth = (int) Math.ceil(Math.log(1.0 / delta));
        this.sketch = new int[depth][width];
        
        // Initialize hash function parameters
        Random random = new Random();
        hashA = new int[depth];
        hashB = new int[depth];
        
        for (int i = 0; i < depth; i++) {
            hashA[i] = random.nextInt(LARGE_PRIME);
            hashB[i] = random.nextInt(LARGE_PRIME);
        }
    }
    
    // Hash function for row i
    private int hash(String item, int i) {
        int hash = item.hashCode();
        return Math.abs((hashA[i] * hash + hashB[i]) % LARGE_PRIME) % width;
    }
    
    // Update count for item
    public void update(String item, int count) {
        for (int i = 0; i < depth; i++) {
            int col = hash(item, i);
            sketch[i][col] += count;
        }
    }
    
    public void update(String item) {
        update(item, 1);
    }
    
    // Estimate count for item
    public int estimate(String item) {
        int minCount = Integer.MAX_VALUE;
        for (int i = 0; i < depth; i++) {
            int col = hash(item, i);
            minCount = Math.min(minCount, sketch[i][col]);
        }
        return minCount;
    }
}

// Usage examples
CountMinSketch cms = new CountMinSketch(0.01, 0.01); // 1% error, 99% confidence

String[] stream = {"apple", "banana", "apple", "cherry", "banana", "apple"};

for (String item : stream) {
    cms.update(item);
}

System.out.println("apple: " + cms.estimate("apple"));     // Should be close to 3
System.out.println("banana: " + cms.estimate("banana"));   // Should be close to 2
System.out.println("cherry: " + cms.estimate("cherry"));   // Should be close to 1
```

## Python Snippet

```python
import math, random

class CountMinSketch:
    LARGE_PRIME = 982451653
    def __init__(self, eps, delta):
        self.w = int(math.ceil(math.e/eps))
        self.d = int(math.ceil(math.log(1.0/delta)))
        self.sk = [[0]*self.w for _ in range(self.d)]
        rng = random.Random(0xC0FFEE)
        self.A = [rng.randrange(1, self.LARGE_PRIME) for _ in range(self.d)]
        self.B = [rng.randrange(0, self.LARGE_PRIME) for _ in range(self.d)]
    def _h(self, s, i):
        h = hash(s) & 0x7FFFFFFF
        return ((self.A[i]*h + self.B[i]) % self.LARGE_PRIME) % self.w
    def update(self, s, c=1):
        for i in range(self.d):
            self.sk[i][self._h(s, i)] += c
    def estimate(self, s):
        return min(self.sk[i][self._h(s, i)] for i in range(self.d))
```

## When to Use

- Real-time analytics on streaming data
- Network traffic analysis and monitoring
- Heavy hitters detection in logs
- Approximate frequency counting with memory constraints

## Trade-offs

**Pros:**

- Constant memory usage regardless of stream size
- Fast updates and queries O(k)
- Guaranteed error bounds
- Mergeable across distributed systems
- No false negatives

**Cons:**

- Only provides upper bound estimates
- May overestimate frequencies
- Requires tuning of parameters (ε, δ)
- Cannot delete items
- Hash collisions cause errors

## Practice Problems

- **Top K Frequent Elements**: Use CMS for streaming version
- **Data Stream Analysis**: Frequency estimation in logs
- **Heavy Hitters**: Find most frequent items in stream
- **Network Monitoring**: Track packet frequencies
- **Real-time Analytics**: Approximate counting systems

<details>
<summary>Implementation Notes (Advanced)</summary>

### Parameter Selection

- **Width w**: w = ⌈e/ε⌉ where ε is relative error
- **Depth d**: d = ⌈ln(1/δ)⌉ where δ is failure probability
- **Memory**: O(ε⁻¹ log δ⁻¹) space complexity
- **Trade-offs**: Larger sketch = better accuracy, more memory

### Hash Function Design

- **Universal hashing**: Use family of hash functions
- **Pairwise independent**: Sufficient for theoretical guarantees
- **Practical choices**: Multiply-shift, polynomial, or cryptographic
- **Collision handling**: Multiple hash functions reduce collisions

### Error Analysis

- **Upper bound**: estimate ≤ true_count + ε × total_count
- **Confidence**: Pr[error > bound] ≤ δ
- **No false negatives**: Never underestimate if item exists
- **Practical error**: Often much smaller than theoretical bound

### Applications

- **Network monitoring**: DDoS detection, traffic analysis
- **Database systems**: Query optimization, statistics
- **Web analytics**: Page view counting, user tracking
- **Security**: Anomaly detection, intrusion prevention

</details>
