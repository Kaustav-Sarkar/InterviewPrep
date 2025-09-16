# Bloom Filter

## Quick Definition

Space-efficient probabilistic data structure for membership testing. Can have false positives but never false negatives. Uses multiple hash functions and bit array.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add | **O(k)** | O(m) |
| Contains | **O(k)** | — |
| False Positive Rate | ~(1-e^(-kn/m))^k | — |
*k = hash functions, m = bit array size, n = elements*

## Core Operations

```java
import java.util.BitSet;
import java.util.List;
import java.util.Arrays;

class BloomFilter {
    private BitSet bitSet;
    private int bitSetSize;
    private int numHashFunctions;
    private int numElements;
    
    public BloomFilter(int expectedElements, double falsePositiveRate) {
        // Optimal bit array size: m = -n*ln(p) / (ln(2)^2)
        this.bitSetSize = (int) Math.ceil(-expectedElements * Math.log(falsePositiveRate) 
                                         / (Math.log(2) * Math.log(2)));
        
        // Optimal number of hash functions: k = m/n * ln(2)
        this.numHashFunctions = (int) Math.ceil(bitSetSize * Math.log(2) / expectedElements);
        
        this.bitSet = new BitSet(bitSetSize);
        this.numElements = 0;
    }
    
    public BloomFilter(int bitSetSize, int numHashFunctions) {
        this.bitSetSize = bitSetSize;
        this.numHashFunctions = numHashFunctions;
        this.bitSet = new BitSet(bitSetSize);
        this.numElements = 0;
    }
    
    // Add element to bloom filter
    public void add(String element) {
        for (int i = 0; i < numHashFunctions; i++) {
            int hash = hash(element, i);
            bitSet.set(Math.abs(hash % bitSetSize));
        }
        numElements++;
    }
    
    // Check if element might be in set
    public boolean mightContain(String element) {
        for (int i = 0; i < numHashFunctions; i++) {
            int hash = hash(element, i);
            if (!bitSet.get(Math.abs(hash % bitSetSize))) {
                return false;  // definitely not in set
            }
        }
        return true;  // might be in set
    }
    
    // Multiple hash functions using single hash + salt
    private int hash(String element, int salt) {
        return (element.hashCode() + salt * 31) * 31;
    }
    
    // Alternative: use different hash algorithms
    private int[] getHashes(String element) {
        int hash1 = element.hashCode();
        int hash2 = hash1 >>> 16;
        
        int[] hashes = new int[numHashFunctions];
        for (int i = 0; i < numHashFunctions; i++) {
            hashes[i] = Math.abs(hash1 + i * hash2);
        }
        return hashes;
    }
    
    // Get current false positive probability
    public double getFalsePositiveRate() {
        double ratio = (double) bitSet.cardinality() / bitSetSize;
        return Math.pow(ratio, numHashFunctions);
    }
    
    // Estimate number of elements (with saturation)
    public int estimatedSize() {
        int bitsSet = bitSet.cardinality();
        if (bitsSet == 0) return 0;
        
        double ratio = (double) bitsSet / bitSetSize;
        if (ratio >= 1.0) return Integer.MAX_VALUE;  // saturated
        
        return (int) (-bitSetSize * Math.log(1 - ratio) / numHashFunctions);
    }
}

// Usage examples
BloomFilter bf = new BloomFilter(1000, 0.01);  // 1000 elements, 1% false positive rate

// Add elements
List<String> urls = Arrays.asList("google.com", "github.com", "stackoverflow.com");
for (String url : urls) {
    bf.add(url);
}

// Test membership
System.out.println(bf.mightContain("google.com"));     // true (definitely in set)
System.out.println(bf.mightContain("facebook.com"));   // false (definitely not in set)
System.out.println(bf.mightContain("twitter.com"));    // might be false positive

// Web crawler duplicate URL detection
class WebCrawler {
    private BloomFilter visitedUrls;
    private Set<String> confirmedUrls;  // for handling false positives
    
    public WebCrawler(int expectedUrls) {
        visitedUrls = new BloomFilter(expectedUrls, 0.001);  // 0.1% false positive
        confirmedUrls = new HashSet<>();
    }
    
    public boolean shouldVisit(String url) {
        if (!visitedUrls.mightContain(url)) {
            return true;  // definitely not visited
        }
        return !confirmedUrls.contains(url);  // check for false positive
    }
    
    public void markVisited(String url) {
        visitedUrls.add(url);
        confirmedUrls.add(url);
    }
}

// Counting Bloom Filter (supports deletion)
class CountingBloomFilter {
    private int[][] counters;  // array of counters instead of bits
    private int bitSetSize, numHashFunctions;
    
    public CountingBloomFilter(int bitSetSize, int numHashFunctions) {
        this.bitSetSize = bitSetSize;
        this.numHashFunctions = numHashFunctions;
        this.counters = new int[bitSetSize][1];
    }
    
    public void add(String element) {
        for (int i = 0; i < numHashFunctions; i++) {
            int hash = Math.abs((element.hashCode() + i * 31) % bitSetSize);
            counters[hash][0]++;
        }
    }
    
    public void remove(String element) {
        for (int i = 0; i < numHashFunctions; i++) {
            int hash = Math.abs((element.hashCode() + i * 31) % bitSetSize);
            if (counters[hash][0] > 0) {
                counters[hash][0]--;
            }
        }
    }
    
    public boolean mightContain(String element) {
        for (int i = 0; i < numHashFunctions; i++) {
            int hash = Math.abs((element.hashCode() + i * 31) % bitSetSize);
            if (counters[hash][0] == 0) return false;
        }
        return true;
    }
}
```

## Python Snippet

```python
import math
from hashlib import blake2b

class BloomFilter:
    def __init__(self, n, p):
        m = int(math.ceil(-n * math.log(p) / (math.log(2)**2)))
        k = int(math.ceil(m / n * math.log(2)))
        self.m, self.k = m, k
        self.bits = bytearray((m + 7)//8)
    def _hashes(self, s):
        h = blake2b(s.encode(), digest_size=16).digest()
        x = int.from_bytes(h[:8], 'big'); y = int.from_bytes(h[8:], 'big')
        for i in range(self.k):
            yield (x + i*y) % self.m
    def add(self, s):
        for idx in self._hashes(s):
            self.bits[idx//8] |= (1 << (idx % 8))
    def might_contain(self, s):
        for idx in self._hashes(s):
            if not (self.bits[idx//8] & (1 << (idx % 8))):
                return False
        return True
```

## When to Use

- Web crawlers for duplicate URL detection
- Database query optimization (check before expensive lookup)
- Distributed systems for reducing network calls
- Cache layers to avoid cache misses
- Spam filtering and malware detection

## Trade-offs

**Pros:**

- Extremely space-efficient
- Fast O(k) operations
- No false negatives
- Scales well with data size

**Cons:**

- False positives possible (tunable rate)
- Cannot delete elements (standard version)
- Cannot retrieve stored elements
- Performance degrades as filter fills up

## Practice Problems

- **Design Web Crawler**: Use bloom filter to avoid revisiting URLs
- **Implement Magic Dictionary**: Bloom filter for fast negative lookups
- **Design Search Autocomplete**: Bloom filter to pre-check suggestions
- **Distributed Cache**: Bloom filter to reduce network calls
- **Spam Detection**: Combine multiple bloom filters for feature detection

<details>
<summary>Implementation Notes (Advanced)</summary>

### Optimal Parameters

- **Bit array size**: m = -n*ln(p) / (ln(2))^2
- **Hash functions**: k = (m/n) * ln(2)
- **False positive rate**: p ≈ (1 - e^(-kn/m))^k
- **Memory efficiency**: ~1.44 log2(1/ε) bits per element

### Hash Function Design

- **Double hashing**: h(x,i) = h1(x) + i*h2(x) mod m
- **Multiple functions**: Different seeds/salts for single hash function
- **Quality matters**: Poor hash functions increase false positive rate
- **Murmur hash**: Often preferred for bloom filters

### Variants and Extensions

- **Counting Bloom Filter**: Supports deletion using counters
- **Scalable Bloom Filter**: Grows dynamically with constant false positive rate
- **Compressed Bloom Filter**: Reduces memory using compression
- **Partitioned Bloom Filter**: Better cache performance

### Performance Considerations

- **Memory access patterns**: Random access can be cache-unfriendly
- **Hash computation cost**: Balance number of functions vs computation
- **Saturation**: Performance degrades as bit array fills
- **Load factor**: Optimal around 50% of bits set

</details>
