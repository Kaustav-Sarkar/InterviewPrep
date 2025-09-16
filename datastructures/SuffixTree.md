# Suffix Tree

## Quick Definition

Compressed trie containing all suffixes of a string. Each edge represents a substring, enabling linear-time string operations like pattern matching and longest common substring finding.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | **O(n)** | O(n) |
| Pattern Search | **O(m)** | — |
| All Occurrences | O(m + k) | — |
| Longest Repeated | **O(n)** | — |

*n = string length, m = pattern length, k = number of occurrences*

## Core Operations

```java
class SuffixTreeNode {
    Map<Character, SuffixTreeNode> children;
    int start, end;     // Edge label indices
    SuffixTreeNode suffixLink;
    int suffixIndex;    // For leaf nodes
    
    public SuffixTreeNode(int start, int end) {
        this.children = new HashMap<>();
        this.start = start;
        this.end = end;
        this.suffixIndex = -1;
    }
}

class SuffixTree {
    private String text;
    private SuffixTreeNode root;
    
    public SuffixTree(String text) {
        this.text = text + "$";
        this.root = new SuffixTreeNode(-1, -1);
        buildSuffixTree();
    }
    
    // Search for pattern in O(m) time
    public boolean contains(String pattern) {
        SuffixTreeNode current = root;
        int patternIndex = 0;
        
        while (patternIndex < pattern.length()) {
            char c = pattern.charAt(patternIndex);
            if (!current.children.containsKey(c)) {
                return false;
            }
            
            SuffixTreeNode next = current.children.get(c);
            // Match characters along the edge
            for (int i = next.start; i <= next.end && patternIndex < pattern.length(); i++) {
                if (text.charAt(i) != pattern.charAt(patternIndex)) {
                    return false;
                }
                patternIndex++;
            }
            current = next;
        }
        return true;
    }
    
    // Find longest repeated substring
    public String longestRepeatedSubstring() {
        // Find internal node with maximum string depth
        // that has at least 2 leaf descendants
        return findLongestRepeated(root, "");
    }
    
    // Count distinct substrings in O(n)
    public int countDistinctSubstrings() {
        return countSubstrings(root);
    }
}

// Usage example
String text = "banana";
SuffixTree st = new SuffixTree(text);

System.out.println("Contains 'ana': " + st.contains("ana"));
System.out.println("Longest repeated: '" + st.longestRepeatedSubstring() + "'");
System.out.println("Distinct substrings: " + st.countDistinctSubstrings());

// Compare with naive approach
System.out.println("Naive contains: " + text.contains("ana"));
```

## Python Snippet

```python
# Simplified search using suffix array as a practical alternative
def build_suffix_array(s):
    s += '$'
    return sorted(range(len(s)), key=lambda i: s[i:])

def contains(s, pat):
    sa = build_suffix_array(s)
    import bisect
    lo, hi = 0, len(sa)
    while lo < hi:
        mid = (lo+hi)//2
        if s[sa[mid]:] >= pat:
            hi = mid
        else:
            lo = mid + 1
    i = lo
    return i < len(sa) and s[sa[i]:].startswith(pat)
```

## When to Use

- Bioinformatics and DNA sequence analysis
- String matching with multiple pattern queries
- Longest common substring problems
- Text indexing for search engines
- Plagiarism detection systems

## Trade-offs

**Pros:**

- Linear time pattern matching O(m)
- Supports complex string queries efficiently
- All suffixes accessible in linear time
- Excellent for multiple queries on same text
- Optimal time complexity for many string problems

**Cons:**

- Complex implementation (Ukkonen's algorithm)
- High space overhead (up to 20x text size)
- Construction complexity makes it impractical for simple cases
- Not suitable for dynamic strings
- Poor cache performance due to pointer structure

## Practice Problems

- **Longest Duplicate Substring**: Find longest repeated substring
- **Longest Common Substring**: Between multiple strings
- **Pattern Matching**: Multiple pattern searches
- **Distinct Subsequences**: Count distinct string patterns
- **Palindromic Substrings**: Find all palindromes efficiently

<details>
<summary>Implementation Notes (Advanced)</summary>

### Ukkonen's Algorithm

- **Linear construction**: O(n) time and space
- **Online algorithm**: Processes string character by character
- **Suffix links**: Key optimization for linear time
- **Active point**: Maintains current position during construction

### Space Optimization

- **Edge compression**: Store indices instead of strings
- **Implicit representation**: Use global end for all leaves
- **Memory layout**: Consider cache-friendly implementations
- **Practical considerations**: Often 10-20x larger than input

### Applications

- **Bioinformatics**: DNA/RNA sequence analysis
- **Information retrieval**: Full-text indexing
- **Data compression**: Finding repeated patterns
- **Computational biology**: Genome assembly and comparison

### Comparison with Alternatives

- **vs Suffix Array**: Tree has better query time, array uses less space
- **vs Trie**: Suffix tree is compressed, handles all suffixes
- **vs Hash tables**: Tree supports range queries, hashing doesn't
- **Implementation choice**: Suffix array often preferred in practice

</details>
