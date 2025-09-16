# Ternary Search Tree

## Quick Definition

Space-efficient trie where each node has three children (less, equal, greater) based on character comparison. Combines trie functionality with BST-like structure.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** avg | O(n) |
| Insert | **O(log n)** avg | — |
| Delete | **O(log n)** avg | — |
| Prefix Match | O(k + log n) | — |

*k = key length, n = number of strings*

## Core Operations

```java
class TSTNode {
    char character;
    boolean isEndOfWord;
    Object value;  // for key-value storage
    TSTNode left, middle, right;
    
    public TSTNode(char character) {
        this.character = character;
        this.isEndOfWord = false;
        this.value = null;
    }
}

class TernarySearchTree {
    private TSTNode root;
    
    public void put(String key, Object value) {
        root = putHelper(root, key, value, 0);
    }
    
    private TSTNode putHelper(TSTNode node, String key, Object value, int index) {
        char c = key.charAt(index);
        
        if (node == null) {
            node = new TSTNode(c);
        }
        
        if (c < node.character) {
            node.left = putHelper(node.left, key, value, index);
        } else if (c > node.character) {
            node.right = putHelper(node.right, key, value, index);
        } else {
            if (index < key.length() - 1) {
                node.middle = putHelper(node.middle, key, value, index + 1);
            } else {
                node.isEndOfWord = true;
                node.value = value;
            }
        }
        
        return node;
    }
    
    public Object get(String key) {
        TSTNode node = getHelper(root, key, 0);
        return (node != null && node.isEndOfWord) ? node.value : null;
    }
    
    private TSTNode getHelper(TSTNode node, String key, int index) {
        if (node == null) return null;
        
        char c = key.charAt(index);
        
        if (c < node.character) {
            return getHelper(node.left, key, index);
        } else if (c > node.character) {
            return getHelper(node.right, key, index);
        } else {
            if (index == key.length() - 1) {
                return node;
            } else {
                return getHelper(node.middle, key, index + 1);
            }
        }
    }
    
    public boolean contains(String key) {
        return get(key) != null;
    }
    
    // Get all keys with given prefix
    public List<String> keysWithPrefix(String prefix) {
        List<String> results = new ArrayList<>();
        TSTNode prefixNode = getHelper(root, prefix, 0);
        
        if (prefixNode != null) {
            if (prefixNode.isEndOfWord) {
                results.add(prefix);
            }
            collectKeys(prefixNode.middle, prefix, results);
        }
        
        return results;
    }
    
    private void collectKeys(TSTNode node, String prefix, List<String> results) {
        if (node == null) return;
        
        collectKeys(node.left, prefix, results);
        
        String newPrefix = prefix + node.character;
        if (node.isEndOfWord) {
            results.add(newPrefix);
        }
        collectKeys(node.middle, newPrefix, results);
        
        collectKeys(node.right, prefix, results);
    }
    
    // Longest prefix match
    public String longestPrefixOf(String query) {
        int length = longestPrefixHelper(root, query, 0, 0);
        return query.substring(0, length);
    }
    
    private int longestPrefixHelper(TSTNode node, String query, int index, int length) {
        if (node == null || index >= query.length()) {
            return length;
        }
        
        char c = query.charAt(index);
        
        if (c < node.character) {
            return longestPrefixHelper(node.left, query, index, length);
        } else if (c > node.character) {
            return longestPrefixHelper(node.right, query, index, length);
        } else {
            if (node.isEndOfWord) {
                length = index + 1;
            }
            return longestPrefixHelper(node.middle, query, index + 1, length);
        }
    }
    
    // Get all keys
    public List<String> keys() {
        List<String> results = new ArrayList<>();
        collectAll(root, "", results);
        return results;
    }
    
    private void collectAll(TSTNode node, String prefix, List<String> results) {
        if (node == null) return;
        
        collectAll(node.left, prefix, results);
        
        String currentPrefix = prefix + node.character;
        if (node.isEndOfWord) {
            results.add(currentPrefix);
        }
        collectAll(node.middle, currentPrefix, results);
        
        collectAll(node.right, prefix, results);
    }
}

// Autocomplete system using TST
class TSTAutocomplete {
    private TernarySearchTree tst;
    
    public TSTAutocomplete(String[] dictionary) {
        tst = new TernarySearchTree();
        for (String word : dictionary) {
            tst.put(word, word);
        }
    }
    
    public List<String> getSuggestions(String prefix, int maxResults) {
        List<String> suggestions = tst.keysWithPrefix(prefix);
        return suggestions.size() > maxResults ? 
               suggestions.subList(0, maxResults) : suggestions;
    }
    
    public String longestMatch(String query) {
        return tst.longestPrefixOf(query);
    }
}

// Symbol table implementation
class TSTSymbolTable<T> {
    private TernarySearchTree tst;
    
    public TSTSymbolTable() {
        tst = new TernarySearchTree();
    }
    
    public void put(String key, T value) {
        tst.put(key, value);
    }
    
    @SuppressWarnings("unchecked")
    public T get(String key) {
        return (T) tst.get(key);
    }
    
    public boolean contains(String key) {
        return tst.contains(key);
    }
    
    public List<String> keys() {
        return tst.keys();
    }
}

// Simple word dictionary using standard collections
class HashMapDictionary {
    private Set<String> words;
    
    public HashMapDictionary(String[] dictionary) {
        words = new HashSet<>(Arrays.asList(dictionary));
    }
    
    public boolean contains(String word) {
        return words.contains(word);
    }
    
    public List<String> getWordsWithPrefix(String prefix) {
        return words.stream()
                   .filter(word -> word.startsWith(prefix))
                   .collect(Collectors.toList());
    }
}

// Usage examples
TernarySearchTree tst = new TernarySearchTree();
String[] words = {"apple", "app", "application", "apply", "apt", "banana", "band", "bandana"};

// Insert words
for (String word : words) {
    tst.put(word, word);
}

System.out.println("Search 'app': " + tst.contains("app"));        // true
System.out.println("Search 'appl': " + tst.contains("appl"));      // false

System.out.println("Keys with prefix 'app': " + tst.keysWithPrefix("app"));
// [app, apple, application, apply]

System.out.println("Longest prefix of 'applications': " + tst.longestPrefixOf("applications"));
// application

System.out.println("All keys: " + tst.keys());

// Autocomplete example
TSTAutocomplete autocomplete = new TSTAutocomplete(words);
List<String> suggestions = autocomplete.getSuggestions("ban", 3);
System.out.println("Autocomplete for 'ban': " + suggestions);
// [banana, band, bandana]

// Symbol table example
TSTSymbolTable<Integer> symbolTable = new TSTSymbolTable<>();
symbolTable.put("apple", 5);
symbolTable.put("banana", 6);
symbolTable.put("cherry", 6);

System.out.println("Value for 'apple': " + symbolTable.get("apple")); // 5
System.out.println("Contains 'grape': " + symbolTable.contains("grape")); // false
```

## Python Snippet

```python
class TSTNode:
    __slots__ = ("ch","end","val","lo","eq","hi")
    def __init__(self, ch):
        self.ch=ch; self.end=False; self.val=None
        self.lo=self.eq=self.hi=None

class TernarySearchTree:
    def __init__(self): self.root=None
    def put(self, key, value=None):
        def rec(node, i):
            c = key[i]
            if not node: node = TSTNode(c)
            if c < node.ch: node.lo = rec(node.lo, i)
            elif c > node.ch: node.hi = rec(node.hi, i)
            elif i+1 < len(key): node.eq = rec(node.eq, i+1)
            else: node.end=True; node.val=value
            return node
        if key: self.root = rec(self.root, 0)
    def get(self, key):
        node=self.root; i=0
        while node and i < len(key):
            c=key[i]
            node = node.lo if c < node.ch else node.hi if c > node.ch else (node.eq if (i:=i+1) else node)  # advance when equal
        return node.val if node and node.end and i==len(key) else None
    def contains(self, key): return self.get(key) is not None
    def keys_with_prefix(self, prefix):
        res=[]; node=self.root; i=0
        while node and i < len(prefix):
            c=prefix[i]
            if c < node.ch: node=node.lo
            elif c > node.ch: node=node.hi
            else: i+=1; node=node.eq if i < len(prefix) else node
        def collect(n, cur):
            if not n: return
            collect(n.lo, cur)
            cur2 = cur + n.ch
            if n.end: res.append(cur2)
            collect(n.eq, cur2)
            collect(n.hi, cur)
        if node:
            if i == len(prefix) and node.end: res.append(prefix)
            collect(node.eq, prefix)
        return res
```

## When to Use

- Dictionary and spell-checker implementations
- Autocomplete systems with limited memory
- Symbol tables in compilers/interpreters
- Prefix matching in networking
- Space-efficient string storage

## Trade-offs

**Pros:**

- More space-efficient than standard trie
- Faster than hash tables for prefix operations  
- Good cache locality compared to Patricia trie
- Supports range queries on strings
- Natural string ordering

**Cons:**

- More complex than hash tables
- Slower than hash tables for exact lookups
- Requires balanced structure for good performance
- Worst-case O(n) for degenerate strings

## Practice Problems

- **Implement Trie (Prefix Tree)**: TST variant implementation
- **Word Search II**: Board game with TST dictionary
- **Search Autocomplete System**: TST-based suggestions
- **Longest Word in Dictionary**: Prefix matching with TST
- **Replace Words**: Dictionary root replacement

<details>
<summary>Implementation Notes (Advanced)</summary>

### Space Efficiency

- **Memory usage**: ~4x less than standard trie for typical strings
- **Node structure**: Only 3 pointers vs 26+ in standard trie
- **Character storage**: One character per node vs edge labels
- **Overhead**: Better for sparse alphabets

### Performance Characteristics

- **Height**: Proportional to string length and alphabet distribution  
- **Cache behavior**: Better locality than Patricia trie
- **Balancing**: Can benefit from randomization or restructuring
- **Degeneration**: Worst case when strings are lexicographically sorted

### Implementation Variants

- **Randomized TST**: Random insertion order for better balance
- **Compressed TST**: Combine with path compression
- **Threaded TST**: Add parent pointers for efficient traversal
- **Persistent TST**: Functional programming version

### Comparison with Alternatives

- **vs Hash Tables**: TST supports prefix operations, Hash is faster for exact match
- **vs Standard Trie**: TST uses less space, Trie has better worst-case
- **vs Patricia Trie**: TST has better cache locality, Patricia more compressed
- **vs Suffix Trees**: TST for dictionaries, Suffix trees for text indexing

</details>
