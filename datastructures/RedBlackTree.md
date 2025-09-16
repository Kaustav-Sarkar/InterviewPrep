# Red-Black Tree

## Quick Definition

Self-balancing binary search tree where nodes are colored red or black with specific properties ensuring O(log n) height. Widely used in standard libraries.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Traverse | O(n) | — |

## Core Operations

```java
// Red-Black Tree node with color
enum Color { RED, BLACK }

class RBNode {
    int data;
    Color color;
    RBNode left, right, parent;
    
    public RBNode(int data) {
        this.data = data;
        this.color = Color.RED;  // new nodes are red
        this.left = this.right = this.parent = null;
    }
}

class RedBlackTree {
    private RBNode root;
    private RBNode NIL;
    
    public RedBlackTree() {
        NIL = new RBNode(0);
        NIL.color = Color.BLACK;
        root = NIL;
    }
    
    // Left rotate
    private void leftRotate(RBNode x) {
        RBNode y = x.right;
        x.right = y.left;
        if (y.left != NIL) {
            y.left.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }
    
    // Right rotate
    private void rightRotate(RBNode x) {
        RBNode y = x.left;
        x.left = y.right;
        if (y.right != NIL) {
            y.right.parent = x;
        }
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }
    
    // Insert and fix violations
    public void insert(int key) {
        RBNode node = new RBNode(key);
        node.left = NIL;
        node.right = NIL;
        
        RBNode y = null;
        RBNode x = root;
        
        // Standard BST insertion
        while (x != NIL) {
            y = x;
            if (node.data < x.data) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        
        node.parent = y;
        if (y == null) {
            root = node;
        } else if (node.data < y.data) {
            y.left = node;
        } else {
            y.right = node;
        }
        
        if (node.parent == null) {
            node.color = Color.BLACK;
            return;
        }
        
        if (node.parent.parent == null) {
            return;
        }
        
        insertFixup(node);
    }
    
    // Fix red-black tree violations after insertion
    private void insertFixup(RBNode k) {
        RBNode u;
        
        while (k.parent.color == Color.RED) {
            if (k.parent == k.parent.parent.right) {
                u = k.parent.parent.left;  // uncle
                
                if (u.color == Color.RED) {
                    // Case 1: uncle is red
                    u.color = Color.BLACK;
                    k.parent.color = Color.BLACK;
                    k.parent.parent.color = Color.RED;
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.left) {
                        // Case 2: uncle is black, k is left child
                        k = k.parent;
                        rightRotate(k);
                    }
                    // Case 3: uncle is black, k is right child
                    k.parent.color = Color.BLACK;
                    k.parent.parent.color = Color.RED;
                    leftRotate(k.parent.parent);
                }
            } else {
                u = k.parent.parent.right;  // uncle
                
                if (u.color == Color.RED) {
                    // Case 1: uncle is red
                    u.color = Color.BLACK;
                    k.parent.color = Color.BLACK;
                    k.parent.parent.color = Color.RED;
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.right) {
                        // Case 2: uncle is black, k is right child
                        k = k.parent;
                        leftRotate(k);
                    }
                    // Case 3: uncle is black, k is left child
                    k.parent.color = Color.BLACK;
                    k.parent.parent.color = Color.RED;
                    rightRotate(k.parent.parent);
                }
            }
            
            if (k == root) {
                break;
            }
        }
        root.color = Color.BLACK;
    }
    
    // Search for a value
    public boolean search(int key) {
        return searchHelper(root, key) != NIL;
    }
    
    private RBNode searchHelper(RBNode node, int key) {
        if (node == NIL || key == node.data) {
            return node;
        }
        
        if (key < node.data) {
            return searchHelper(node.left, key);
        }
        return searchHelper(node.right, key);
    }
    
    // Inorder traversal
    public void inorder() {
        inorderHelper(root);
    }
    
    private void inorderHelper(RBNode node) {
        if (node != NIL) {
            inorderHelper(node.left);
            System.out.print(node.data + "(" + (node.color == Color.RED ? "R" : "B") + ") ");
            inorderHelper(node.right);
        }
    }
}

// Using Java's TreeSet/TreeMap (Red-Black tree implementation)
TreeSet<Integer> rbSet = new TreeSet<>();
rbSet.add(10); rbSet.add(5); rbSet.add(15);
rbSet.add(3); rbSet.add(7); rbSet.add(12); rbSet.add(20);

// TreeSet provides all red-black tree benefits
System.out.println("Contains 7: " + rbSet.contains(7));     // true
System.out.println("First: " + rbSet.first());              // 3
System.out.println("Last: " + rbSet.last());                // 20
System.out.println("Lower than 10: " + rbSet.lower(10));    // 7
System.out.println("Higher than 10: " + rbSet.higher(10));  // 12

// TreeMap for key-value pairs
TreeMap<Integer, String> rbMap = new TreeMap<>();
rbMap.put(10, "ten");
rbMap.put(5, "five");
rbMap.put(15, "fifteen");

// Navigation in TreeMap
System.out.println("Floor key of 12: " + rbMap.floorKey(12));    // 10
System.out.println("Ceiling key of 12: " + rbMap.ceilingKey(12)); // 15

// Range operations
NavigableMap<Integer, String> subMap = rbMap.subMap(5, true, 15, false);
System.out.println("SubMap [5, 15): " + subMap);

// Usage example
RedBlackTree rbt = new RedBlackTree();
int[] values = {7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13};
for (int val : values) {
    rbt.insert(val);
}

System.out.println("Inorder traversal:");
rbt.inorder();  // Shows values with colors
System.out.println("\nSearch 10: " + rbt.search(10));  // true
System.out.println("Search 5: " + rbt.search(5));    // false
```

## Python Snippet

```python
# Minimal API using sortedcontainers (if available) or fallback to bisect list
try:
    from sortedcontainers import SortedSet
    rb = SortedSet()
    rb.add(10); rb.add(5); rb.add(15)
    _ = 7 in rb
except Exception:
    import bisect
    class RBSet:
        def __init__(self): self.a = []
        def add(self, x):
            i = bisect.bisect_left(self.a, x)
            if i == len(self.a) or self.a[i] != x: self.a.insert(i, x)
        def contains(self, x):
            i = bisect.bisect_left(self.a, x); return i < len(self.a) and self.a[i] == x
    rb = RBSet(); rb.add(10); rb.add(5); rb.add(15)
```

## When to Use

- Standard library implementations (Java TreeSet/TreeMap)
- Applications requiring guaranteed O(log n) performance
- Persistent data structures (immutable variants)
- Systems programming (Linux kernel, databases)
- When fewer rotations than AVL trees are preferred

## Trade-offs

**Pros:**

- Guaranteed O(log n) operations
- Fewer rotations than AVL trees
- Used in standard libraries
- Good balance between search and update performance
- Self-balancing without height tracking

**Cons:**

- Complex implementation with many cases
- Color tracking overhead
- Slightly deeper than AVL trees
- More complex deletion algorithm

## Practice Problems

- **Design Red-Black Tree**: Implement insert with rebalancing
- **Validate Binary Search Tree**: Check BST properties
- **Kth Smallest in BST**: Tree traversal problems
- **Range Sum of BST**: BST range queries
- **Serialize and Deserialize BST**: Tree reconstruction

<details>
<summary>Implementation Notes (Advanced)</summary>

### Red-Black Properties

1. **Node color**: Every node is either red or black
2. **Root property**: Root is always black
3. **Red property**: Red nodes have black children only
4. **Black property**: All paths from root to null have same black node count
5. **Leaf property**: All leaves (NIL) are black

### Insertion Cases

- **Case 1**: Uncle is red → recolor
- **Case 2**: Uncle is black, triangle → rotate to line
- **Case 3**: Uncle is black, line → rotate and recolor

### Deletion Complexity

- **Red node deletion**: Simple, no violations
- **Black node deletion**: May violate black property
- **Fixup cases**: 4 complex cases for rebalancing
- **Double black**: Conceptual extra black to maintain property

### Standard Library Usage

- **Java TreeSet/TreeMap**: Red-black tree implementation
- **C++ std::set/map**: Usually red-black trees
- **Performance**: Slightly slower search than AVL, faster updates
- **Memory**: One bit per node for color storage

### Comparison with AVL

- **Height difference**: Red-black ≤ 2 × AVL height
- **Rotations**: Red-black has fewer rotations on updates
- **Use cases**: Red-black for frequent updates, AVL for frequent searches

</details>
