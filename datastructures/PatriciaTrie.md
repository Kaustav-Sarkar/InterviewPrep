# Patricia Trie (Radix Tree)

## Quick Definition

Compressed trie where nodes with single children are merged into parent, storing edge labels. Space-efficient for string storage with common prefixes.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(k)** | O(n) |
| Insert | **O(k)** | — |
| Delete | **O(k)** | — |
| Prefix Match | O(k) | — |

*k = key length, n = total characters stored*

## Core Operations

```java
class PatriciaNode {
    Map<Character, PatriciaNode> children;
    String edge;  // compressed edge label
    boolean isEndOfWord;
    String value;  // optional value for key-value storage
    
    public PatriciaNode() {
        this.children = new HashMap<>();
        this.edge = "";
        this.isEndOfWord = false;
        this.value = null;
    }
    
    public PatriciaNode(String edge) {
        this();
        this.edge = edge;
    }
}

class PatriciaTrie {
    private PatriciaNode root;
    
    public PatriciaTrie() {
        root = new PatriciaNode();
    }
    
    public void insert(String word) {
        insert(word, null);
    }
    
    public void insert(String key, String value) {
        PatriciaNode current = root;
        int i = 0;
        
        while (i < key.length()) {
            char ch = key.charAt(i);
            
            if (!current.children.containsKey(ch)) {
                // Create new node with remaining suffix
                String remainingSuffix = key.substring(i);
                PatriciaNode newNode = new PatriciaNode(remainingSuffix);
                newNode.isEndOfWord = true;
                newNode.value = value;
                current.children.put(ch, newNode);
                return;
            }
            
            PatriciaNode child = current.children.get(ch);
            String edge = child.edge;
            int commonLength = longestCommonPrefix(key.substring(i), edge);
            
            if (commonLength == edge.length()) {
                // Full edge matches, continue to next node
                i += commonLength;
                current = child;
            } else {
                // Split the edge
                splitEdge(current, ch, child, commonLength, key.substring(i), value);
                return;
            }
        }
        
        current.isEndOfWord = true;
        current.value = value;
    }
    
    private int longestCommonPrefix(String s1, String s2) {
        int i = 0;
        while (i < s1.length() && i < s2.length() && s1.charAt(i) == s2.charAt(i)) {
            i++;
        }
        return i;
    }
    
    public boolean search(String word) {
        PatriciaNode node = searchNode(word);
        return node != null && node.isEndOfWord;
    }
    
    public boolean startsWith(String prefix) {
        PatriciaNode current = root;
        int i = 0;
        
        while (i < prefix.length() && current != null) {
            char ch = prefix.charAt(i);
            
            if (!current.children.containsKey(ch)) {
                return false;
            }
            
            PatriciaNode child = current.children.get(ch);
            String edge = child.edge;
            String remaining = prefix.substring(i);
            
            if (remaining.length() <= edge.length()) {
                return edge.startsWith(remaining);
            }
            
            if (remaining.startsWith(edge)) {
                i += edge.length();
                current = child;
            } else {
                return false;
            }
        }
        
        return true;
    }
    
    private PatriciaNode searchNode(String key) {
        PatriciaNode current = root;
        int i = 0;
        
        while (i < key.length() && current != null) {
            char ch = key.charAt(i);
            
            if (!current.children.containsKey(ch)) {
                return null;
            }
            
            PatriciaNode child = current.children.get(ch);
            String edge = child.edge;
            
            if (key.substring(i).startsWith(edge)) {
                i += edge.length();
                current = child;
            } else {
                return null;
            }
        }
        
        return current;
    }
}

// Autocomplete system using Patricia Trie
class AutocompleteSystem {
    private PatriciaTrie trie;
    
    public AutocompleteSystem(String[] dictionary) {
        trie = new PatriciaTrie();
        for (String word : dictionary) {
            trie.insert(word);
        }
    }
    
    public boolean hasPrefix(String prefix) {
        return trie.startsWith(prefix);
    }
    
    public void addWord(String word) {
        trie.insert(word);
    }
}

// Usage examples
PatriciaTrie trie = new PatriciaTrie();
String[] words = {"car", "card", "care", "careful", "cars", "cat", "cats"};

for (String word : words) {
    trie.insert(word);
}

System.out.println("Search 'car': " + trie.search("car"));       // true
System.out.println("Search 'ca': " + trie.search("ca"));         // false
System.out.println("Starts with 'car': " + trie.startsWith("car")); // true

// Autocomplete example
AutocompleteSystem autocomplete = new AutocompleteSystem(words);
System.out.println("Has prefix 'ca': " + autocomplete.hasPrefix("ca")); // true
```

## Python Snippet

```python
class Node:
    def __init__(self, edge=""):
        self.edge = edge
        self.end = False
        self.val = None
        self.ch = {}

class PatriciaTrie:
    def __init__(self):
        self.root = Node()
    def insert(self, key, value=None):
        cur = self.root; i = 0
        while i < len(key):
            c = key[i]
            if c not in cur.ch:
                n = Node(key[i:]); n.end = True; n.val = value; cur.ch[c] = n; return
            child = cur.ch[c]; edge = child.edge
            j = 0
            while i + j < len(key) and j < len(edge) and key[i+j] == edge[j]:
                j += 1
            if j == len(edge):
                cur = child; i += j
            else:
                # split
                mid = Node(edge[:j])
                mid.ch[edge[j]] = child
                child.edge = edge[j:]
                cur.ch[c] = mid
                if i + j == len(key):
                    mid.end = True; mid.val = value
                else:
                    rest = key[i+j:]
                    n = Node(rest); n.end = True; n.val = value
                    mid.ch[rest[0]] = n
                return
        cur.end = True; cur.val = value
    def search(self, key):
        cur = self.root; i = 0
        while i < len(key):
            c = key[i]
            if c not in cur.ch: return False
            child = cur.ch[c]; edge = child.edge
            if key[i:].startswith(edge):
                i += len(edge); cur = child
            else: return False
        return cur.end
```

## When to Use

- Autocomplete and typeahead systems
- IP routing tables and network prefix matching
- Dictionary and spell-checker implementations
- String matching with common prefixes
- Memory-efficient storage of strings with overlap

## Trade-offs

**Pros:**

- Space-efficient for strings with common prefixes
- Fast prefix-based operations
- Supports longest prefix matching
- Memory savings over standard trie
- Excellent for autocomplete systems

**Cons:**

- More complex implementation than standard trie
- Edge splitting adds complexity
- Worst-case still dependent on string lengths
- Less cache-friendly than arrays for small datasets

## Practice Problems

- **Implement Trie (Prefix Tree)**: Enhanced with compression
- **Word Search II**: Board game with Patricia trie
- **Longest Common Prefix**: Use trie structure
- **Design Search Autocomplete System**: Patricia trie backend
- **IP Routing**: Longest prefix matching

<details>
<summary>Implementation Notes (Advanced)</summary>

### Compression Techniques

- **Edge compression**: Merge single-child chains into edges
- **Path compression**: Store entire suffixes when possible
- **Lazy expansion**: Decompress only when necessary
- **Alphabet reduction**: Optimize for specific character sets

### Memory Optimization

- **Compact node representation**: Minimize per-node overhead
- **Shared suffixes**: Detect and merge common endings
- **Lazy deletion**: Mark nodes as deleted without immediate removal
- **Memory pooling**: Reuse node objects

### Performance Considerations

- **String operations**: Minimize substring creation
- **Cache locality**: Consider node layout for better cache performance
- **Batch operations**: Optimize for bulk insertions

### Real-world Applications

- **DNS resolution**: Domain name prefix matching
- **Network routing**: BGP prefix tables
- **Text indexing**: Search engines and databases
- **Code completion**: IDE autocomplete systems

</details>
