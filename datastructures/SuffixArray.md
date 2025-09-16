# Suffix Array

## Quick Definition

Array of integers representing the lexicographic order of all suffixes of a string. Enables efficient string processing and pattern matching with compact representation.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | **O(n log n)** | O(n) |
| Pattern Search | **O(m log n)** | — |
| LCP Construction | **O(n)** | O(n) |
| Longest Repeated | **O(n)** | — |

*n = string length, m = pattern length*

## Core Operations

```java
class SuffixArray {
    private String text;
    private int[] suffixArray;
    private int[] lcp; // Longest Common Prefix array
    private int n;
    
    public SuffixArray(String text) {
        this.text = text + "$"; // Add sentinel
        this.n = this.text.length();
        this.suffixArray = buildSuffixArray();
        this.lcp = buildLCPArray();
    }
    
    // Build suffix array using O(n log n) approach
    private int[] buildSuffixArray() {
        Integer[] suffixes = new Integer[n];
        for (int i = 0; i < n; i++) {
            suffixes[i] = i;
        }
        
        // Sort suffixes lexicographically
        Arrays.sort(suffixes, (i, j) -> {
            return text.substring(i).compareTo(text.substring(j));
        });
        
        return Arrays.stream(suffixes).mapToInt(i -> i).toArray();
    }
    
    // Binary search for pattern
    public boolean contains(String pattern) {
        return countOccurrences(pattern) > 0;
    }
    
    public int countOccurrences(String pattern) {
        int left = findFirst(pattern);
        if (left == -1) return 0;
        int right = findLast(pattern);
        return right - left + 1;
    }
    
    // Find longest repeated substring using LCP array
    public String longestRepeatedSubstring() {
        int maxLen = 0;
        int maxIndex = 0;
        
        for (int i = 1; i < n; i++) {
            if (lcp[i] > maxLen) {
                maxLen = lcp[i];
                maxIndex = suffixArray[i];
            }
        }
        
        return maxLen > 0 ? text.substring(maxIndex, maxIndex + maxLen) : "";
    }
    
    // Count distinct substrings
    public long countDistinctSubstrings() {
        long total = (long) n * (n - 1) / 2; // Total substrings
        long duplicates = 0;
        
        for (int i = 1; i < n; i++) {
            duplicates += lcp[i];
        }
        
        return total - duplicates;
    }
}

// Usage example
String text = "banana";
SuffixArray sa = new SuffixArray(text);

System.out.println("Pattern 'ana' found: " + sa.contains("ana"));
System.out.println("Longest repeated: '" + sa.longestRepeatedSubstring() + "'");
System.out.println("Distinct substrings: " + sa.countDistinctSubstrings());

// Compare with naive O(n²) approach
Set<String> naive = new HashSet<>();
for (int i = 0; i < text.length(); i++) {
    for (int j = i + 1; j <= text.length(); j++) {
        naive.add(text.substring(i, j));
    }
}
System.out.println("Naive distinct count: " + naive.size());
```

## Python Snippet

```python
def build_suffix_array(s):
    s += '$'
    return sorted(range(len(s)), key=lambda i: s[i:])

def contains(sa, s, pat):
    import bisect
    n = len(sa)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo+hi)//2
        if s[sa[mid]:].startswith(pat) or s[sa[mid]:] > pat:
            hi = mid
        else:
            lo = mid + 1
    i = lo
    return i < n and s[sa[i]:].startswith(pat)
```

## When to Use

- Pattern matching in large texts
- Bioinformatics sequence analysis
- Text indexing and search engines
- String algorithms requiring suffix ordering
- Longest common substring problems

## Trade-offs

**Pros:**

- Space-efficient compared to suffix trees
- Fast pattern searching with preprocessing
- Supports complex string queries
- Linear space complexity O(n)
- Good for static text analysis

**Cons:**

- Construction time O(n log n) or O(n log²n)
- Complex implementation for optimal algorithms
- Not suitable for dynamic text
- Requires additional structures (LCP) for some operations
- Less intuitive than suffix trees

## Practice Problems

- **Longest Duplicate Substring**: Find longest repeated substring
- **Shortest Superstring**: Overlapping string concatenation
- **Count Different Palindromic Subsequences**: Advanced string analysis
- **Pattern Matching**: Multiple pattern searches
- **String Matching in Array**: Suffix-based string comparison

<details>
<summary>Implementation Notes (Advanced)</summary>

### Construction Algorithms

- **Naive O(n² log n)**: Sort all suffixes directly
- **DC3/SKEW O(n)**: Linear time construction
- **SA-IS O(n)**: Induced sorting algorithm
- **Radix sort approach**: O(n log n) with good constants

### LCP Array Construction

- **Kasai's algorithm**: O(n) time using suffix array
- **Direct construction**: Computed during suffix array building
- **Applications**: Used for many string queries
- **Space optimization**: Can be computed on-demand

### Pattern Searching

- **Binary search**: O(m log n) for pattern of length m
- **Two-phase search**: Find range then extract positions
- **Multiple patterns**: Batch processing optimization
- **Wildcards**: Extended pattern matching

### Applications

- **Bioinformatics**: DNA/protein sequence analysis
- **Information retrieval**: Text indexing and search
- **Data compression**: Finding repeated patterns
- **Plagiarism detection**: Document similarity analysis

</details>
