# Cuckoo Filter

## Quick Definition

Space-efficient probabilistic data structure for approximate membership testing that supports deletion. Uses cuckoo hashing with fingerprints to achieve better space efficiency than Bloom filters.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Insert | **O(1)** | O(n) |
| Delete | **O(1)** | — |
| Lookup | **O(1)** | — |
| False Positive Rate | — | ε ≈ 2^(-f) |

*f = fingerprint size in bits*

## Core Operations

```java
import java.util.Random;

class CuckooFilter {
    private byte[][] table;
    private int numBuckets;
    private int bucketSize;
    private int fingerprintSize;
    private int maxKicks;
    private Random random;
    
    public CuckooFilter(int capacity, int fingerprintSize) {
        this.fingerprintSize = fingerprintSize;
        this.bucketSize = 4; // typical bucket size
        this.numBuckets = capacity / bucketSize;
        this.table = new byte[numBuckets][bucketSize];
        this.maxKicks = 500; // maximum cuckoo kicks
        this.random = new Random();
    }
    
    // Primary hash function
    private int hash1(String item) {
        return Math.abs(item.hashCode()) % numBuckets;
    }
    
    // Generate fingerprint
    private byte fingerprint(String item) {
        int hash = item.hashCode();
        return (byte) (hash & ((1 << fingerprintSize) - 1));
    }
    
    // Secondary hash using fingerprint
    private int hash2(int bucket, byte fingerprint) {
        return bucket ^ hash(fingerprint);
    }
    
    private int hash(byte fingerprint) {
        return Math.abs(fingerprint) % numBuckets;
    }
    
    // Insert item into filter
    public boolean insert(String item) {
        byte fp = fingerprint(item);
        int bucket1 = hash1(item);
        int bucket2 = hash2(bucket1, fp);
        
        // Try to insert in bucket1
        if (insertInBucket(bucket1, fp)) {
            return true;
        }
        
        // Try to insert in bucket2
        if (insertInBucket(bucket2, fp)) {
            return true;
        }
        
        // Perform cuckoo eviction
        int evictBucket = random.nextBoolean() ? bucket1 : bucket2;
        return cuckooInsert(evictBucket, fp);
    }
    
    private boolean insertInBucket(int bucket, byte fingerprint) {
        for (int i = 0; i < bucketSize; i++) {
            if (table[bucket][i] == 0) {
                table[bucket][i] = fingerprint;
                return true;
            }
        }
        return false;
    }
    
    private boolean cuckooInsert(int bucket, byte fingerprint) {
        for (int kicks = 0; kicks < maxKicks; kicks++) {
            // Pick random entry in bucket
            int entry = random.nextInt(bucketSize);
            byte oldFingerprint = table[bucket][entry];
            table[bucket][entry] = fingerprint;
            
            if (oldFingerprint == 0) {
                return true; // Found empty slot
            }
            
            // Calculate alternative bucket for evicted fingerprint
            fingerprint = oldFingerprint;
            bucket = hash2(bucket, fingerprint);
            
            // Try to place in alternative bucket
            if (insertInBucket(bucket, fingerprint)) {
                return true;
            }
        }
        
        return false; // Failed to insert after max kicks
    }
    
    // Check if item might be in filter
    public boolean contains(String item) {
        byte fp = fingerprint(item);
        int bucket1 = hash1(item);
        int bucket2 = hash2(bucket1, fp);
        
        return bucketContains(bucket1, fp) || bucketContains(bucket2, fp);
    }
    
    private boolean bucketContains(int bucket, byte fingerprint) {
        for (int i = 0; i < bucketSize; i++) {
            if (table[bucket][i] == fingerprint) {
                return true;
            }
        }
        return false;
    }
    
    // Delete item from filter
    public boolean delete(String item) {
        byte fp = fingerprint(item);
        int bucket1 = hash1(item);
        int bucket2 = hash2(bucket1, fp);
        
        return deleteFromBucket(bucket1, fp) || deleteFromBucket(bucket2, fp);
    }
    
    private boolean deleteFromBucket(int bucket, byte fingerprint) {
        for (int i = 0; i < bucketSize; i++) {
            if (table[bucket][i] == fingerprint) {
                table[bucket][i] = 0;
                return true;
            }
        }
        return false;
    }
    
    // Get load factor
    public double getLoadFactor() {
        int occupied = 0;
        for (int i = 0; i < numBuckets; i++) {
            for (int j = 0; j < bucketSize; j++) {
                if (table[i][j] != 0) {
                    occupied++;
                }
            }
        }
        return (double) occupied / (numBuckets * bucketSize);
    }
    
    // Clear the filter
    public void clear() {
        for (int i = 0; i < numBuckets; i++) {
            for (int j = 0; j < bucketSize; j++) {
                table[i][j] = 0;
            }
        }
    }
}

// Simplified implementation using HashSet for comparison
class SimpleMembershipTest {
    private HashSet<String> exactSet;
    private int maxSize;
    
    public SimpleMembershipTest(int maxSize) {
        this.exactSet = new HashSet<>();
        this.maxSize = maxSize;
    }
    
    public boolean insert(String item) {
        if (exactSet.size() >= maxSize) {
            return false;
        }
        return exactSet.add(item);
    }
    
    public boolean contains(String item) {
        return exactSet.contains(item);
    }
    
    public boolean delete(String item) {
        return exactSet.remove(item);
    }
    
    public int size() {
        return exactSet.size();
    }
}

// Usage examples
CuckooFilter filter = new CuckooFilter(1000, 8); // 1000 capacity, 8-bit fingerprints

// Insert items
String[] items = {"apple", "banana", "cherry", "date", "elderberry"};
for (String item : items) {
    boolean inserted = filter.insert(item);
    System.out.println("Inserted " + item + ": " + inserted);
}

// Test membership
for (String item : items) {
    boolean contains = filter.contains(item);
    System.out.println("Contains " + item + ": " + contains);
}

// Test false positives
String[] testItems = {"fig", "grape", "kiwi"};
for (String item : testItems) {
    boolean contains = filter.contains(item);
    System.out.println("Contains " + item + " (should be false): " + contains);
}

// Test deletion
filter.delete("banana");
System.out.println("After deleting banana, contains banana: " + filter.contains("banana"));

System.out.println("Load factor: " + filter.getLoadFactor());

// Compare with exact set
SimpleMembershipTest exactTest = new SimpleMembershipTest(1000);
for (String item : items) {
    exactTest.insert(item);
}

System.out.println("\\nComparison with exact set:");
System.out.println("Exact set size: " + exactTest.size());
System.out.println("Cuckoo filter load factor: " + filter.getLoadFactor());
```

## Python Snippet

```python
import random, hashlib

class CuckooFilter:
    def __init__(self, capacity, fp_bits=8, bucket_size=4, max_kicks=500):
        self.fp_bits = fp_bits; self.bucket_size = bucket_size
        self.max_kicks = max_kicks; self.n_buckets = max(1, capacity // bucket_size)
        self.table = [[0]*bucket_size for _ in range(self.n_buckets)]
        self.rng = random.Random(42)
    def _fp(self, s):
        h = hashlib.blake2b(s.encode(), digest_size=2).digest()
        v = int.from_bytes(h, 'big') & ((1<<self.fp_bits)-1)
        return v or 1
    def _h1(self, s):
        return hash(s) & 0x7FFFFFFF % self.n_buckets
    def _h2(self, i, fp):
        return (i ^ (hash(fp) & 0x7FFFFFFF)) % self.n_buckets
    def _insert_bucket(self, b, fp):
        for i in range(self.bucket_size):
            if self.table[b][i] == 0:
                self.table[b][i] = fp; return True
        return False
    def insert(self, s):
        fp = self._fp(s); b1 = self._h1(s); b2 = self._h2(b1, fp)
        if self._insert_bucket(b1, fp) or self._insert_bucket(b2, fp): return True
        b = self.rng.choice([b1, b2])
        for _ in range(self.max_kicks):
            i = self.rng.randrange(self.bucket_size)
            fp, self.table[b][i] = self.table[b][i], fp
            b = self._h2(b, fp)
            if self._insert_bucket(b, fp): return True
        return False
    def contains(self, s):
        fp = self._fp(s); b1 = self._h1(s); b2 = self._h2(b1, fp)
        return fp in self.table[b1] or fp in self.table[b2]
    def delete(self, s):
        fp = self._fp(s); b1 = self._h1(s); b2 = self._h2(b1, fp)
        for b in (b1, b2):
            for i in range(self.bucket_size):
                if self.table[b][i] == fp:
                    self.table[b][i] = 0; return True
        return False
```

## When to Use

- Distributed systems requiring membership testing
- Network security and spam filtering
- Database query optimization
- Cache systems with limited memory
- Applications requiring item deletion

## Trade-offs

**Pros:**

- Better space efficiency than Bloom filters
- Supports deletion operations
- Bounded false positive rate
- Good cache performance with buckets
- No false negatives

**Cons:**

- May fail to insert due to hash collisions
- More complex than Bloom filters
- Requires careful parameter tuning
- Still has false positives (though fewer)
- Not suitable for counting

## Practice Problems

- **Design Membership System**: Implement space-efficient membership test
- **URL Filtering**: Block malicious URLs with limited memory
- **Cache Optimization**: Pre-filter database queries
- **Duplicate Detection**: Find duplicates in data streams
- **Distributed Caching**: Coordinate cache invalidation

<details>
<summary>Implementation Notes (Advanced)</summary>

### Parameter Selection

- **Bucket size**: Typically 2-8 entries per bucket
- **Fingerprint size**: Balance between false positive rate and space
- **Load factor**: Keep below 95% for good performance
- **Number of buckets**: Should be power of 2 for efficiency

### Cuckoo Hashing

- **Maximum kicks**: Limit eviction attempts to avoid infinite loops
- **Eviction strategy**: Random eviction vs. oldest first
- **Hash quality**: Good hash functions crucial for distribution
- **Collision handling**: Fallback strategies when cuckoo fails

### Space Efficiency

- **Memory layout**: Pack fingerprints efficiently
- **Compression**: Use smaller fingerprints when possible
- **Overhead**: Account for metadata and alignment
- **Comparison**: vs Bloom filter space usage

### Performance Optimization

- **Cache optimization**: Bucket-based design improves locality
- **SIMD operations**: Vectorize bucket operations
- **Memory prefetching**: Prefetch alternative bucket
- **Batch operations**: Process multiple items together

</details>
