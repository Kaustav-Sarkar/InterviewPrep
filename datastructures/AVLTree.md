# AVL Tree

## Quick Definition

Self-balancing binary search tree where height difference between left and right subtrees of any node is at most 1. Guarantees O(log n) operations through rotations.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Traverse | O(n) | — |

## Core Operations

```java
class AVLNode {
    int val, height;
    AVLNode left, right;
    
    AVLNode(int val) {
        this.val = val;
        this.height = 1;
    }
}

class AVLTree {
    private AVLNode root;
    
    // Get height of node
    private int height(AVLNode node) {
        return node == null ? 0 : node.height;
    }
    
    // Get balance factor
    private int getBalance(AVLNode node) {
        return node == null ? 0 : height(node.left) - height(node.right);
    }
    
    // Update height of node
    private void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(height(node.left), height(node.right));
        }
    }
    
    // Right rotate
    private AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;
        
        // Perform rotation
        x.right = y;
        y.left = T2;
        
        // Update heights
        updateHeight(y);
        updateHeight(x);
        
        return x;  // new root
    }
    
    // Left rotate
    private AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;
        
        // Perform rotation
        y.left = x;
        x.right = T2;
        
        // Update heights
        updateHeight(x);
        updateHeight(y);
        
        return y;  // new root
    }
    
    // Insert value
    public void insert(int val) {
        root = insert(root, val);
    }
    
    private AVLNode insert(AVLNode node, int val) {
        // Standard BST insertion
        if (node == null) return new AVLNode(val);
        
        if (val < node.val) {
            node.left = insert(node.left, val);
        } else if (val > node.val) {
            node.right = insert(node.right, val);
        } else {
            return node;  // duplicate values not allowed
        }
        
        // Update height
        updateHeight(node);
        
        // Get balance factor
        int balance = getBalance(node);
        
        // Left Left Case
        if (balance > 1 && val < node.left.val) {
            return rightRotate(node);
        }
        
        // Right Right Case
        if (balance < -1 && val > node.right.val) {
            return leftRotate(node);
        }
        
        // Left Right Case
        if (balance > 1 && val > node.left.val) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }
        
        // Right Left Case
        if (balance < -1 && val < node.right.val) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }
        
        return node;  // unchanged
    }
    
    // Search for value
    public boolean search(int val) {
        return search(root, val);
    }
    
    private boolean search(AVLNode node, int val) {
        if (node == null) return false;
        if (val == node.val) return true;
        return val < node.val ? search(node.left, val) : search(node.right, val);
    }
}

// Usage with Java's TreeSet (self-balancing)
TreeSet<Integer> avlSet = new TreeSet<>();
avlSet.addAll(Arrays.asList(10, 20, 30, 40, 50, 25));
System.out.println(avlSet);  // [10, 20, 25, 30, 40, 50]

// TreeMap for key-value pairs
TreeMap<Integer, String> avlMap = new TreeMap<>();
avlMap.put(30, "thirty");
avlMap.put(10, "ten");
avlMap.put(50, "fifty");
```

## Python Snippet

```python
class AVLNode:
    def __init__(self, val):
        self.val = val; self.left = None; self.right = None; self.h = 1

def height(n): return n.h if n else 0
def bal(n): return height(n.left) - height(n.right) if n else 0
def upd(n): n.h = 1 + max(height(n.left), height(n.right))

def rot_right(y):
    x, T2 = y.left, y.left.right
    x.right, y.left = y, T2
    upd(y); upd(x); return x

def rot_left(x):
    y, T2 = x.right, x.right.left
    y.left, x.right = x, T2
    upd(x); upd(y); return y

def insert(node, val):
    if not node: return AVLNode(val)
    if val < node.val: node.left = insert(node.left, val)
    elif val > node.val: node.right = insert(node.right, val)
    else: return node
    upd(node)
    b = bal(node)
    if b > 1 and val < node.left.val: return rot_right(node)
    if b < -1 and val > node.right.val: return rot_left(node)
    if b > 1 and val > node.left.val:
        node.left = rot_left(node.left); return rot_right(node)
    if b < -1 and val < node.right.val:
        node.right = rot_right(node.right); return rot_left(node)
    return node
```

## When to Use

- Applications requiring guaranteed O(log n) performance
- Real-time systems where worst-case performance matters
- Database indexing with frequent insertions/deletions
- Ordered data with balanced access patterns
- When TreeSet/TreeMap performance is critical

## Trade-offs

**Pros:**

- Guaranteed O(log n) for all operations
- More strictly balanced than Red-Black trees
- Better search performance than Red-Black trees
- Java's TreeSet/TreeMap use balanced trees

**Cons:**

- More rotations during insertion/deletion
- Higher memory overhead (height tracking)
- More complex implementation than basic BST
- Slower insertion/deletion than Red-Black trees

## Practice Problems

- **Validate Binary Search Tree**: Check if tree maintains BST property
- **Balanced Binary Tree**: Verify if tree is height-balanced
- **Convert Sorted Array to BST**: Build balanced BST from sorted array
- **Delete Node in BST**: Handle deletion while maintaining balance
- **Range Sum of BST**: Sum values in given range

<details>
<summary>Implementation Notes (Advanced)</summary>

### Rotation Mechanics

- **Single rotations**: Fix simple imbalances (LL, RR cases)
- **Double rotations**: Fix complex imbalances (LR, RL cases)  
- **Height updates**: Must update heights after rotations
- **Balance factor**: |height(left) - height(right)| ≤ 1

### Java TreeSet/TreeMap

- **Red-Black trees**: Java's implementation uses Red-Black, not AVL
- **Performance**: Slightly different constants, but same O(log n)
- **Self-balancing**: Automatic rebalancing on modifications
- **Ordering**: Natural ordering or custom Comparator

### Memory Considerations

- **Height storage**: Each node stores height (4-8 bytes overhead)
- **Recursive calls**: Stack space O(log n) for operations
- **Cache locality**: Tree traversal can have poor cache performance

</details>
