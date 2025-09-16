# HyperLogLog

## Quick Definition

Probabilistic data structure for estimating cardinality (distinct count) of large datasets using minimal memory. Uses hash functions and leading zero counting for logarithmic space complexity.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add | **O(1)** | O(log log n) |
| Count | **O(m)** | — |
| Merge | **O(m)** | — |
| Error Rate | — | ±1.04/√m |

*m = number of buckets, n = cardinality*

## Core Operations

```java
import java.util.Arrays;

class HyperLogLog {
    private int[] buckets;
    private int bucketCount;
    private int bucketBits;
    private double alpha;
    
    public HyperLogLog(int precision) {
        this.bucketBits = precision;
        this.bucketCount = 1 << precision; // 2^precision
        this.buckets = new int[bucketCount];
        this.alpha = calculateAlpha(bucketCount);
    }
    
    // Calculate alpha constant for bias correction
    private double calculateAlpha(int m) {
        if (m == 16) return 0.673;
        if (m == 32) return 0.697;
        if (m == 64) return 0.709;
        return 0.7213 / (1.0 + 1.079 / m);
    }
    
    // Add item to HyperLogLog
    public void add(String item) {
        long hash = hash64(item);
        
        // Use first bucketBits for bucket selection
        int bucket = (int) (hash & ((1L << bucketBits) - 1));
        
        // Use remaining bits for leading zero count
        long w = hash >>> bucketBits;
        int leadingZeros = leadingZeros(w) + 1;
        
        // Update bucket with maximum leading zeros seen
        buckets[bucket] = Math.max(buckets[bucket], leadingZeros);
    }
    
    // Simple hash function (in practice, use better hash)
    private long hash64(String item) {
        long hash = item.hashCode();
        hash ^= (hash >>> 33);
        hash *= 0xff51afd7ed558ccdL;
        hash ^= (hash >>> 33);
        hash *= 0xc4ceb9fe1a85ec53L;
        hash ^= (hash >>> 33);
        return hash;
    }
    
    // Count leading zeros in a long
    private int leadingZeros(long value) {
        if (value == 0) return 64;
        return Long.numberOfLeadingZeros(value);
    }
    
    // Estimate cardinality
    public long estimate() {
        double rawEstimate = alpha * bucketCount * bucketCount / 
                           Arrays.stream(buckets).mapToDouble(b -> Math.pow(2, -b)).sum();
        
        // Apply bias correction for small estimates
        if (rawEstimate <= 2.5 * bucketCount) {
            int zeros = (int) Arrays.stream(buckets).filter(b -> b == 0).count();
            if (zeros != 0) {
                return Math.round(bucketCount * Math.log(bucketCount / (double) zeros));
            }
        }
        
        // Apply bias correction for large estimates
        if (rawEstimate <= (1.0/30.0) * (1L << 32)) {
            return Math.round(rawEstimate);
        } else {
            return Math.round(-1 * (1L << 32) * Math.log(1 - rawEstimate / (1L << 32)));
        }
    }
    
    // Merge another HyperLogLog into this one
    public void merge(HyperLogLog other) {
        if (this.bucketCount != other.bucketCount) {
            throw new IllegalArgumentException("Cannot merge HLLs with different bucket counts");
        }
        
        for (int i = 0; i < bucketCount; i++) {
            this.buckets[i] = Math.max(this.buckets[i], other.buckets[i]);
        }
    }
    
    // Clear the HyperLogLog
    public void clear() {
        Arrays.fill(buckets, 0);
    }
    
    // Get memory usage in bytes
    public int getMemoryUsage() {
        return bucketCount * 4; // 4 bytes per int bucket
    }
    
    // Get expected error rate
    public double getExpectedError() {
        return 1.04 / Math.sqrt(bucketCount);
    }
}

// Cardinality estimator using HashSet for comparison
class ExactCardinality {
    private HashSet<String> items;
    
    public ExactCardinality() {
        items = new HashSet<>();
    }
    
    public void add(String item) {
        items.add(item);
    }
    
    public long count() {
        return items.size();
    }
    
    public void clear() {
        items.clear();
    }
    
    public int getMemoryUsage() {
        return items.size() * 50; // Rough estimate: 50 bytes per string
    }
}

// Stream cardinality analyzer
class StreamCardinalityAnalyzer {
    private HyperLogLog hll;
    private ExactCardinality exact;
    private long totalItems;
    
    public StreamCardinalityAnalyzer(int precision) {
        hll = new HyperLogLog(precision);
        exact = new ExactCardinality();
        totalItems = 0;
    }
    
    public void processItem(String item) {
        hll.add(item);
        exact.add(item);
        totalItems++;
    }
    
    public void printStats() {
        long hllEstimate = hll.estimate();
        long exactCount = exact.count();
        double error = Math.abs(hllEstimate - exactCount) / (double) exactCount * 100;
        
        System.out.printf("Total items processed: %d%n", totalItems);
        System.out.printf("Exact distinct count: %d%n", exactCount);
        System.out.printf("HLL estimate: %d%n", hllEstimate);
        System.out.printf("Error: %.2f%%%n", error);
        System.out.printf("Expected error: ±%.2f%%%n", hll.getExpectedError() * 100);
        System.out.printf("HLL memory: %d bytes%n", hll.getMemoryUsage());
        System.out.printf("Exact memory: ~%d bytes%n", exact.getMemoryUsage());
    }
}

// Multi-set cardinality tracking
class MultiSetCardinalityTracker {
    private Map<String, HyperLogLog> setEstimators;
    private int precision;
    
    public MultiSetCardinalityTracker(int precision) {
        this.precision = precision;
        this.setEstimators = new HashMap<>();
    }
    
    public void addToSet(String setName, String item) {
        setEstimators.computeIfAbsent(setName, k -> new HyperLogLog(precision)).add(item);
    }
    
    public long getCardinality(String setName) {
        HyperLogLog hll = setEstimators.get(setName);
        return hll != null ? hll.estimate() : 0;
    }
    
    public long getUnionCardinality(String set1, String set2) {
        HyperLogLog hll1 = setEstimators.get(set1);
        HyperLogLog hll2 = setEstimators.get(set2);
        
        if (hll1 == null || hll2 == null) return 0;
        
        // Create temporary HLL for union
        HyperLogLog union = new HyperLogLog(precision);
        union.merge(hll1);
        union.merge(hll2);
        
        return union.estimate();
    }
    
    public void printAllCardinalities() {
        setEstimators.forEach((name, hll) -> 
            System.out.printf("Set '%s': ~%d distinct items%n", name, hll.estimate()));
    }
}

// Usage examples
HyperLogLog hll = new HyperLogLog(12); // 2^12 = 4096 buckets

// Simulate adding many items
Random random = new Random();
for (int i = 0; i < 100000; i++) {
    String item = "user_" + (random.nextInt(50000) + 1); // 50K unique users
    hll.add(item);
}

System.out.println("Estimated cardinality: " + hll.estimate());
System.out.println("Expected error: ±" + (hll.getExpectedError() * 100) + "%");
System.out.println("Memory usage: " + hll.getMemoryUsage() + " bytes");

// Compare with exact counting
StreamCardinalityAnalyzer analyzer = new StreamCardinalityAnalyzer(10);

// Process stream of user IDs
for (int i = 0; i < 10000; i++) {
    String userId = "user_" + (random.nextInt(1000) + 1);
    analyzer.processItem(userId);
}

analyzer.printStats();

// Multi-set example
MultiSetCardinalityTracker tracker = new MultiSetCardinalityTracker(10);

// Add users to different groups
for (int i = 0; i < 5000; i++) {
    String userId = "user_" + (random.nextInt(2000) + 1);
    String group = i % 3 == 0 ? "premium" : (i % 3 == 1 ? "basic" : "trial");
    tracker.addToSet(group, userId);
}

tracker.printAllCardinalities();
System.out.println("Union of premium and basic: " + 
                   tracker.getUnionCardinality("premium", "basic"));

// Merge example
HyperLogLog hll1 = new HyperLogLog(8);
HyperLogLog hll2 = new HyperLogLog(8);

for (int i = 0; i < 1000; i++) {
    hll1.add("item_" + i);
    hll2.add("item_" + (i + 500)); // 500 overlap
}

System.out.println("HLL1 estimate: " + hll1.estimate());
System.out.println("HLL2 estimate: " + hll2.estimate());

hll1.merge(hll2);
System.out.println("Merged estimate: " + hll1.estimate());
System.out.println("Expected: ~1500 (1000 + 1000 - 500 overlap)");
```

## Python Snippet

```python
import math, struct, hashlib

class HyperLogLog:
    def __init__(self, p):
        self.p = p; self.m = 1 << p
        self.reg = [0]*self.m
        self.alpha = 0.7213/(1 + 1.079/self.m) if self.m > 64 else {16:0.673,32:0.697,64:0.709}[self.m]
    def _hash(self, s):
        h = hashlib.blake2b(s.encode(), digest_size=8).digest()
        return struct.unpack('>Q', h)[0]
    def add(self, s):
        x = self._hash(s)
        idx = x & (self.m - 1)
        w = x >> self.p
        rho = (w.bit_length() ^ 63) + 1 if w != 0 else 64
        self.reg[idx] = max(self.reg[idx], rho)
    def estimate(self):
        Z = sum(2.0**-r for r in self.reg)
        E = self.alpha * self.m * self.m / Z
        if E <= 2.5*self.m:
            V = self.reg.count(0)
            if V: return self.m * math.log(self.m/float(V))
        return E
    def merge(self, other):
        assert self.m == other.m
        self.reg = [max(a,b) for a,b in zip(self.reg, other.reg)]
```

## When to Use

- Large-scale analytics and data processing
- Real-time cardinality estimation in streams
- Database query optimization
- Web analytics and user tracking
- Network traffic analysis

## Trade-offs

**Pros:**

- Extremely space-efficient O(log log n)
- Fast O(1) insertion
- Mergeable across distributed systems
- Bounded error rate
- No false negatives or positives

**Cons:**

- Only approximates cardinality
- Cannot retrieve individual items
- Requires careful parameter tuning
- Error increases with smaller datasets
- Cannot delete items

## Practice Problems

- **Unique Visitors**: Count distinct users in web logs
- **Stream Analytics**: Real-time unique event counting
- **Database Optimization**: Estimate join sizes
- **Network Analysis**: Count unique IP addresses
- **A/B Testing**: Compare user set sizes

<details>
<summary>Implementation Notes (Advanced)</summary>

### Mathematical Foundation

- **Hash distribution**: Relies on uniform hash function
- **Leading zeros**: Probability of k leading zeros is 2^(-k)
- **Harmonic mean**: Used to combine bucket estimates
- **Bias correction**: Adjustments for small and large estimates

### Parameter Selection

- **Precision p**: Use p=12-16 for most applications
- **Bucket count**: m = 2^p buckets
- **Memory usage**: m × log₂(log₂(n_max)) bits per bucket
- **Error vs space**: Higher precision = more memory, less error

### Optimization Techniques

- **Sparse representation**: Store only non-zero buckets for small sets
- **Compressed counting**: Use fewer bits per bucket when possible
- **LogLog variants**: SuperLogLog, HyperLogLog++ for better accuracy
- **GPU acceleration**: Parallel processing for large-scale analytics

### Practical Considerations

- **Hash quality**: Use strong hash functions for uniformity
- **Floating point**: Be careful with precision in calculations
- **Bias correction**: Apply appropriate corrections for estimate ranges
- **Distributed merging**: HLLs can be merged across machines

</details>
