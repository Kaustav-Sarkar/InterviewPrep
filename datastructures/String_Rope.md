# String Rope

## Quick Definition

Binary tree structure for efficiently storing and manipulating large strings. Each leaf contains a string fragment and each internal node stores the length of its left subtree for fast indexing.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Concatenate | **O(1)** | O(log n) |
| Index | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Substring | O(log n + k) | O(k) |

*k = length of substring*

## Core Operations

```java
class RopeNode {
    String data;           // for leaf nodes
    int weight;           // length of left subtree + this node's string
    RopeNode left, right; // for internal nodes
    
    public RopeNode(String data) {
        this.data = data;
        this.weight = data.length();
    }
    
    public RopeNode(RopeNode left, RopeNode right) {
        this.data = null;
        this.left = left;
        this.right = right;
        this.weight = (left != null ? left.totalLength() : 0);
    }
    
    public boolean isLeaf() {
        return data != null;
    }
    
    public int totalLength() {
        if (isLeaf()) return data.length();
        return weight + (right != null ? right.totalLength() : 0);
    }
}

class StringRope {
    private RopeNode root;
    
    public StringRope(String str) {
        this.root = new RopeNode(str);
    }
    
    // Get character at index
    public char charAt(int index) {
        return charAt(root, index);
    }
    
    private char charAt(RopeNode node, int index) {
        if (node.isLeaf()) {
            return node.data.charAt(index);
        }
        
        if (index < node.weight) {
            return charAt(node.left, index);
        } else {
            return charAt(node.right, index - node.weight);
        }
    }
    
    // Concatenate two ropes in O(1)
    public StringRope concat(StringRope other) {
        RopeNode newRoot = new RopeNode(this.root, other.root);
        return new StringRope(newRoot);
    }
    
    // Insert string at index
    public StringRope insert(int index, String str) {
        StringRope[] parts = split(index);
        StringRope middle = new StringRope(str);
        return parts[0].concat(middle).concat(parts[1]);
    }
}

// Usage example
StringRope rope = new StringRope("Hello");
StringRope world = new StringRope(" World!");
StringRope combined = rope.concat(world);

System.out.println("Combined: " + combined); // "Hello World!"
System.out.println("Char at 6: " + combined.charAt(6)); // 'W'

StringRope withInsert = combined.insert(5, " Beautiful");
System.out.println("After insert: " + withInsert); // "Hello Beautiful World!"
```

## Python Snippet

```python
class RopeNode:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left; self.right = right
        self.weight = (len(data) if data is not None else (left.weight + (len(left.data) if left and left.data else 0))) if left else (len(data) if data else 0)

    def is_leaf(self): return self.data is not None

def total_length(node):
    if not node: return 0
    if node.is_leaf(): return len(node.data)
    return total_length(node.left) + total_length(node.right)

def char_at(node, idx):
    if node.is_leaf(): return node.data[idx]
    if idx < node.weight: return char_at(node.left, idx)
    return char_at(node.right, idx - node.weight)

def concat(a, b):
    n = RopeNode(None, a, b); n.weight = total_length(a); return n
```

## When to Use

- Text editors with large documents
- String processing with frequent concatenations
- Undo/redo systems for text operations
- Log file manipulation and analysis
- Document version control systems

## Trade-offs

**Pros:**

- Efficient concatenation O(1)
- Good for large strings with frequent edits
- Supports efficient substring operations
- Memory efficient for sparse operations
- Natural undo/redo implementation

**Cons:**

- Complex implementation compared to strings
- Overhead for small strings
- Requires rebalancing for optimal performance
- Not cache-friendly for sequential access
- Higher memory usage per character

## Practice Problems

- **Text Editor Operations**: Implement efficient text editor
- **String Concatenation**: Avoid quadratic concatenation costs
- **Document Diff**: Compare large documents efficiently
- **Log Processing**: Handle large log files with insertions
- **Version Control**: Track document changes over time

<details>
<summary>Implementation Notes (Advanced)</summary>

### Tree Balancing

- **Height balance**: Maintain logarithmic height
- **Weight balance**: Balance by subtree sizes
- **Rebalancing triggers**: When to rebalance the tree
- **Optimal thresholds**: Leaf size and balance factors

### Memory Management

- **String interning**: Reuse common string fragments
- **Lazy concatenation**: Defer actual string operations
- **Memory pooling**: Reuse rope nodes
- **Garbage collection**: Minimize object allocation

### Performance Optimization

- **Caching**: Cache frequently accessed substrings
- **Iterators**: Efficient traversal without full string construction
- **Parallel operations**: Concurrent rope operations
- **Compression**: Compress repeated patterns

### Alternative Implementations

- **Gap buffer**: Different approach for text editors
- **Piece table**: Alternative text editor structure
- **Persistent ropes**: Immutable versions for functional programming
- **Weighted trees**: Different balancing strategies

</details>
