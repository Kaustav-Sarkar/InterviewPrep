# BitSet (Bitmap)

## Quick Definition

Compact array of bits supporting fast bitwise operations. Each bit represents presence/absence of an element. Extremely memory-efficient for dense integer sets.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Set/Clear | **O(1)** | O(n/8) |
| Get | **O(1)** | — |
| AND/OR/XOR | O(n/w) | — |
| Count | O(n/w) | — |
*w = word size (64 bits)*

## Core Operations

```java
import java.util.BitSet;

// Basic BitSet operations
BitSet bitSet = new BitSet(1000);  // capacity for 1000 bits

// Set and clear bits
bitSet.set(5);        // set bit 5 to true
bitSet.set(10, 20);   // set bits 10-19 to true
bitSet.clear(15);     // clear bit 15
bitSet.flip(7);       // toggle bit 7

// Query operations
boolean isSet = bitSet.get(5);           // check if bit 5 is set
int firstSet = bitSet.nextSetBit(0);     // find first set bit from index 0
int firstClear = bitSet.nextClearBit(0); // find first clear bit
int cardinality = bitSet.cardinality();  // count set bits
boolean isEmpty = bitSet.isEmpty();      // check if no bits are set

// Set operations
BitSet set1 = new BitSet();
BitSet set2 = new BitSet();
set1.set(1); set1.set(3); set1.set(5);
set2.set(3); set2.set(5); set2.set(7);

BitSet union = (BitSet) set1.clone();
union.or(set2);        // union: {1, 3, 5, 7}

BitSet intersection = (BitSet) set1.clone();
intersection.and(set2); // intersection: {3, 5}

BitSet difference = (BitSet) set1.clone();
difference.andNot(set2); // difference: {1}

// Sieve of Eratosthenes using BitSet
BitSet sieveOfEratosthenes(int n) {
    BitSet isPrime = new BitSet(n + 1);
    isPrime.set(2, n + 1);  // initially mark all as prime
    
    for (int i = 2; i * i <= n; i++) {
        if (isPrime.get(i)) {
            // Clear multiples of i
            for (int j = i * i; j <= n; j += i) {
                isPrime.clear(j);
            }
        }
    }
    return isPrime;
}

// Custom BitSet wrapper for cleaner API
class IntSet {
    private BitSet bits = new BitSet();
    
    public void add(int x) { bits.set(x); }
    public void remove(int x) { bits.clear(x); }
    public boolean contains(int x) { return bits.get(x); }
    public int size() { return bits.cardinality(); }
    public boolean isEmpty() { return bits.isEmpty(); }
    
    public IntSet union(IntSet other) {
        IntSet result = new IntSet();
        result.bits.or(this.bits);
        result.bits.or(other.bits);
        return result;
    }
    
    public IntSet intersection(IntSet other) {
        IntSet result = new IntSet();
        result.bits.or(this.bits);
        result.bits.and(other.bits);
        return result;
    }
}

// Bit manipulation examples
int[] singleNumber(int[] nums) {
    BitSet seen = new BitSet();
    for (int num : nums) {
        if (seen.get(num + 50000)) {  // offset for negative numbers
            seen.clear(num + 50000);
        } else {
            seen.set(num + 50000);
        }
    }
    return seen.stream().mapToInt(i -> i - 50000).toArray();
}
```

## Python Snippet

```python
# Using Python int as a bitset
class BitSet:
    def __init__(self, n=0): self.bits = 0; self.n = n
    def set(self, i): self.bits |= (1 << i)
    def clear(self, i): self.bits &= ~(1 << i)
    def flip(self, i): self.bits ^= (1 << i)
    def get(self, i): return (self.bits >> i) & 1 == 1
    def count(self): return self.bits.bit_count()

def sieve(n):
    is_prime = [True]*(n+1)
    is_prime[0:2] = [False, False]
    p = 2
    while p*p <= n:
        if is_prime[p]:
            for x in range(p*p, n+1, p): is_prime[x] = False
        p += 1
    return is_prime
```

## When to Use

- Dense sets of small non-negative integers
- Set operations (union, intersection, difference)
- Bit manipulation and flag storage
- Prime number sieves and mathematical algorithms
- Memory-constrained environments requiring compact storage

## Trade-offs

**Pros:**

- Extremely memory-efficient (1 bit per element)
- Fast bitwise operations
- Built-in set operations
- Cache-friendly for dense data

**Cons:**

- Limited to non-negative integers
- Inefficient for sparse sets
- Fixed maximum size considerations
- No direct iteration over elements

## Practice Problems

- **Single Number**: Use XOR operations with bits
- **Repeated DNA Sequences**: BitSet for seen sequences
- **Power of Two**: Bit manipulation checks
- **Maximum XOR**: BitSet with trie-like structure
- **Prime Number Generation**: Sieve of Eratosthenes

<details>
<summary>Implementation Notes (Advanced)</summary>

### Memory Layout

- **Word-based storage**: Typically 64-bit words for efficiency
- **Bit packing**: 8x more memory-efficient than boolean arrays
- **Dynamic growth**: BitSet grows automatically as needed
- **Alignment**: Words aligned for efficient processor access

### Performance Characteristics

- **Bitwise operations**: Highly optimized at processor level
- **Cache efficiency**: Excellent for dense bit patterns
- **SIMD instructions**: Modern processors can parallelize bit operations
- **Population count**: Hardware-accelerated bit counting

### Optimization Techniques

- **Word-level operations**: Process 64 bits at once
- **Branch-free algorithms**: Avoid conditional logic
- **Bit twiddling hacks**: Efficient bit manipulation patterns
- **Sparse representation**: Switch to other structures for sparse data

### Alternative Representations

- **Roaring Bitmaps**: Hybrid approach for sparse/dense regions
- **Compressed BitSets**: Run-length encoding for sparse data
- **Rank/Select structures**: Support for advanced queries

</details>
