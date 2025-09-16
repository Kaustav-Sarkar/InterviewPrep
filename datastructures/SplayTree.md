# Splay Tree

## Quick Definition

Self-adjusting binary search tree that moves frequently accessed nodes closer to root via splaying operations. Provides excellent amortized performance for non-uniform access patterns.

## Big-O Summary

| Operation | Amortized | Worst Case | Space |
|-----------|----------|------------|-------|
| Search | **O(log n)** | O(n) | O(n) |
| Insert | **O(log n)** | O(n) | — |
| Delete | **O(log n)** | O(n) | — |
| Splay | O(log n) | O(n) | — |

## Core Operations

```java
class SplayNode {
    int key;
    SplayNode left, right, parent;
    
    public SplayNode(int key) {
        this.key = key;
        this.left = this.right = this.parent = null;
    }
}

class SplayTree {
    private SplayNode root;
    
    public SplayTree() {
        root = null;
    }
    
    // Splay operation - move node to root
    private void splay(SplayNode x) {
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step: x's parent is root
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step: both x and parent are left children
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step: both x and parent are right children
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else {
                // Zig-zag step: x and parent are different child types
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                    leftRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                    rightRotate(x.parent);
                }
            }
        }
        root = x;
    }
    
    // Search and splay
    public boolean search(int key) {
        SplayNode result = searchHelper(root, key);
        if (result != null) {
            splay(result);
            return true;
        }
        return false;
    }
    
    // Insert and splay
    public void insert(int key) {
        if (root == null) {
            root = new SplayNode(key);
            return;
        }
        
        SplayNode current = root;
        SplayNode parent = null;
        
        while (current != null) {
            parent = current;
            if (key < current.key) {
                current = current.left;
            } else if (key > current.key) {
                current = current.right;
            } else {
                // Key already exists, splay and return
                splay(current);
                return;
            }
        }
        
        SplayNode newNode = new SplayNode(key);
        newNode.parent = parent;
        
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        
        splay(newNode);
    }
    
    // Get root key (last accessed)
    public Integer getRootKey() {
        return root != null ? root.key : null;
    }
}

// Usage examples
SplayTree splay = new SplayTree();
splay.insert(10); splay.insert(5); splay.insert(15);

System.out.println("Search 5: " + splay.search(5));
System.out.println("Root after searching 5: " + splay.getRootKey()); // 5
```

## Python Snippet

```python
class SplayNode:
    def __init__(self, key):
        self.key = key; self.left = None; self.right = None; self.parent = None

def rotate_left(x):
    y = x.right; x.right = y.left
    if y.left: y.left.parent = x
    y.parent = x.parent
    if not x.parent: return y
    if x.parent.left is x: x.parent.left = y
    else: x.parent.right = y
    y.left = x; x.parent = y; return None

def rotate_right(x):
    y = x.left; x.left = y.right
    if y.right: y.right.parent = x
    y.parent = x.parent
    if not x.parent: return y
    if x.parent.left is x: x.parent.left = y
    else: x.parent.right = y
    y.right = x; x.parent = y; return None

def splay(root, x):
    while x.parent:
        p, g = x.parent, x.parent.parent
        if not g:
            if p.left is x: new = rotate_right(p)
            else: new = rotate_left(p)
            if new: root = new
        elif g.left is p and p.left is x:
            _ = rotate_right(g); new = rotate_right(p);  
            if new: root = new
        elif g.right is p and p.right is x:
            _ = rotate_left(g); new = rotate_left(p)
            if new: root = new
        else:
            if p.left is x: _ = rotate_right(p); new = rotate_left(g)
            else: _ = rotate_left(p); new = rotate_right(g)
            if new: root = new
    return root

def bst_insert(root, key):
    if not root: return SplayNode(key)
    cur = root; parent = None
    while cur:
        parent = cur
        cur = cur.left if key < cur.key else (cur.right if key > cur.key else None)
        if cur is None: break
    node = SplayNode(key)
    node.parent = parent
    if key < parent.key: parent.left = node
    elif key > parent.key: parent.right = node
    return splay(root, node)
```

## When to Use

- Applications with non-uniform access patterns
- Caching systems with temporal locality
- Recently accessed data needs fast access
- Simple implementation without complex balancing

## Trade-offs

**Pros:**

- Excellent amortized performance O(log n)
- Self-adjusting to access patterns
- Simple implementation (no color/height tracking)
- Good for temporal locality
- Working set theorem guarantees

**Cons:**

- Poor worst-case performance O(n)
- Can become unbalanced with pathological access
- More rotations than other balanced trees
- Not suitable for concurrent access
- Performance depends heavily on access patterns

## Practice Problems

- **LRU Cache**: Splay tree provides natural LRU behavior
- **Access Frequency**: Self-adjusting based on usage patterns
- **Range Queries**: Split operation for range access
- **Temporal Locality**: Recently accessed items stay near root
- **Adaptive Sorting**: Tree adjusts to input patterns

<details>
<summary>Implementation Notes (Advanced)</summary>

### Splay Operations

- **Zig step**: Single rotation when parent is root
- **Zig-zig step**: Double rotation in same direction
- **Zig-zag step**: Double rotation in different directions
- **Bottom-up splaying**: Start from accessed node

### Amortized Analysis

- **Potential function**: Based on tree structure
- **Working set bound**: O(r log n) for r distinct accesses
- **Dynamic optimality**: Conjectured optimal for any access sequence
- **Competitive ratio**: Within constant factor of optimal BST

### Access Patterns

- **Temporal locality**: Recent accesses are fast
- **Spatial locality**: Nearby keys become closer
- **Frequency**: Frequently accessed nodes migrate toward root
- **Sequential access**: Good performance for sorted access

### Performance Considerations

- **Cache effects**: More rotations can hurt cache performance
- **Memory allocation**: Node creation overhead
- **Recursion depth**: Can be deep for degenerate trees
- **Access tracking**: Monitor access patterns for optimization

</details>
