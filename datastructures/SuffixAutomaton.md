# Suffix Automaton

## Quick Definition

Minimal automaton that accepts all suffixes of a string. Combines the functionality of suffix trees with finite automaton properties, enabling efficient string processing and pattern recognition.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | **O(n)** | O(n) |
| Pattern Search | **O(m)** | — |
| Count Substrings | **O(n)** | — |
| Longest Common | **O(n)** | — |

*n = string length, m = pattern length*

## Core Operations

```java
class SuffixAutomatonNode {
    Map<Character, SuffixAutomatonNode> transitions;
    SuffixAutomatonNode suffixLink;
    int length;           // Length of longest string reaching this state
    int firstOccurrence; // First occurrence position
    
    public SuffixAutomatonNode() {
        this.transitions = new HashMap<>();
        this.suffixLink = null;
        this.length = 0;
        this.firstOccurrence = -1;
    }
}

class SuffixAutomaton {
    private SuffixAutomatonNode root;
    private SuffixAutomatonNode lastState;
    private String text;
    
    public SuffixAutomaton(String text) {
        this.text = text;
        this.root = new SuffixAutomatonNode();
        this.lastState = root;
        buildAutomaton();
    }
    
    // Build suffix automaton incrementally in O(n) time
    private void buildAutomaton() {
        for (int i = 0; i < text.length(); i++) {
            extend(text.charAt(i), i);
        }
    }
    
    // Check if pattern exists in O(m) time
    public boolean contains(String pattern) {
        SuffixAutomatonNode current = root;
        
        for (char c : pattern.toCharArray()) {
            if (!current.transitions.containsKey(c)) {
                return false;
            }
            current = current.transitions.get(c);
        }
        return true;
    }
    
    // Count distinct substrings in O(n) time
    public long countDistinctSubstrings() {
        return countSubstrings(root);
    }
    
    private long countSubstrings(SuffixAutomatonNode state) {
        long count = 0;
        for (SuffixAutomatonNode next : state.transitions.values()) {
            count += 1 + countSubstrings(next);
        }
        return count;
    }
    
    // Find longest common substring with another string
    public String longestCommonSubstring(String other) {
        int maxLength = 0;
        int endPosition = 0;
        
        SuffixAutomatonNode current = root;
        int currentLength = 0;
        
        for (int i = 0; i < other.length(); i++) {
            char c = other.charAt(i);
            
            while (current != null && !current.transitions.containsKey(c)) {
                current = current.suffixLink;
                currentLength = (current != null) ? current.length : 0;
            }
            
            if (current != null) {
                current = current.transitions.get(c);
                currentLength++;
                
                if (currentLength > maxLength) {
                    maxLength = currentLength;
                    endPosition = i;
                }
            } else {
                current = root;
                currentLength = 0;
            }
        }
        
        return maxLength > 0 ? 
               other.substring(endPosition - maxLength + 1, endPosition + 1) : "";
    }
}

// Usage example
String text = "ababa";
SuffixAutomaton sa = new SuffixAutomaton(text);

System.out.println("Pattern 'aba' found: " + sa.contains("aba"));
System.out.println("Distinct substrings: " + sa.countDistinctSubstrings());
System.out.println("LCS with 'babab': '" + sa.longestCommonSubstring("babab") + "'");

// Compare with simple approach
System.out.println("Simple contains: " + text.contains("aba"));
```

## Python Snippet

```python
class State:
    def __init__(self):
        self.next = {}
        self.link = -1
        self.len = 0

class SuffixAutomaton:
    def __init__(self):
        self.st = [State()]
        self.last = 0
    def extend(self, c):
        cur = len(self.st); self.st.append(State())
        self.st[cur].len = self.st[self.last].len + 1
        p = self.last
        while p != -1 and c not in self.st[p].next:
            self.st[p].next[c] = cur; p = self.st[p].link
        if p == -1:
            self.st[cur].link = 0
        else:
            q = self.st[p].next[c]
            if self.st[p].len + 1 == self.st[q].len:
                self.st[cur].link = q
            else:
                clone = len(self.st); self.st.append(State())
                self.st[clone].len = self.st[p].len + 1
                self.st[clone].next = self.st[q].next.copy()
                self.st[clone].link = self.st[q].link
                while p != -1 and self.st[p].next.get(c, -1) == q:
                    self.st[p].next[c] = clone; p = self.st[p].link
                self.st[q].link = self.st[cur].link = clone
        self.last = cur
    def build(self, s):
        for ch in s: self.extend(ch)
    def contains(self, pat):
        v = 0
        for ch in pat:
            if ch not in self.st[v].next: return False
            v = self.st[v].next[ch]
        return True
```

## When to Use

- Advanced string matching with multiple patterns
- Lexicographic string analysis
- String compression and pattern discovery
- Computational biology sequence analysis
- Text processing requiring substring enumeration

## Trade-offs

**Pros:**

- Linear construction time O(n)
- Optimal for substring counting problems
- Supports complex string queries efficiently
- Minimal automaton representation
- Excellent for lexicographic operations

**Cons:**

- Complex implementation and theory
- High space overhead (similar to suffix trees)
- Requires deep understanding of automaton theory
- Not intuitive for simple string operations
- Limited practical applications

## Practice Problems

- **Distinct Subsequences**: Count all distinct subsequences
- **Lexicographically Smallest String**: Find kth smallest substring
- **String Matching**: Advanced pattern matching problems
- **Longest Common Substring**: Between multiple strings
- **Palindromic Substrings**: Enhanced palindrome detection

<details>
<summary>Implementation Notes (Advanced)</summary>

### Construction Algorithm

- **Incremental construction**: Build automaton character by character
- **State cloning**: Handle overlapping suffixes correctly
- **Suffix links**: Maintain failure transitions for efficiency
- **Minimality**: Ensures minimal number of states

### Mathematical Properties

- **State count**: At most 2n-1 states for string of length n
- **Transition count**: At most 3n-4 transitions
- **Equivalence classes**: States represent equivalence classes of suffixes
- **Right languages**: Each state accepts a specific set of suffixes

### Applications

- **String algorithms**: Advanced substring problems
- **Pattern matching**: Multiple pattern matching
- **Text compression**: Finding repetitive structures
- **Bioinformatics**: DNA sequence analysis

### Comparison with Alternatives

- **vs Suffix Tree**: Similar functionality, different structure
- **vs Suffix Array**: Automaton better for online queries
- **vs Trie**: Handles all suffixes, not just prefixes
- **Practical use**: Primarily theoretical, suffix arrays more common

</details>
