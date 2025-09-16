# Treap

## Quick Definition

Randomized binary search tree where each node has both a key (for BST property) and a random priority (for heap property). Combines BST ordering with heap balancing.

## Big-O Summary

| Operation | Time (Expected) | Space |
|-----------|----------------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Split/Merge | O(log n) | — |

## Core Operations

```java
import java.util.Random;

class TreapNode {
    int key;
    int priority;
    TreapNode left, right;
    
    public TreapNode(int key) {
        this.key = key;
        this.priority = new Random().nextInt(100000);
        this.left = this.right = null;
    }
    
    public TreapNode(int key, int priority) {
        this.key = key;
        this.priority = priority;
        this.left = this.right = null;
    }
}

class Treap {
    private TreapNode root;
    private Random random;
    
    public Treap() {
        root = null;
        random = new Random();
    }
    
    // Right rotate
    private TreapNode rightRotate(TreapNode y) {
        TreapNode x = y.left;
        y.left = x.right;
        x.right = y;
        return x;
    }
    
    // Left rotate
    private TreapNode leftRotate(TreapNode x) {
        TreapNode y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }
    
    public void insert(int key) {
        root = insertHelper(root, key);
    }
    
    private TreapNode insertHelper(TreapNode node, int key) {
        // Base case: create new node
        if (node == null) {
            return new TreapNode(key);
        }
        
        // Duplicate key
        if (key == node.key) {
            return node;
        }
        
        // Insert in left or right subtree
        if (key < node.key) {
            node.left = insertHelper(node.left, key);
            
            // Maintain heap property: parent priority ≥ child priority
            if (node.left.priority > node.priority) {
                node = rightRotate(node);
            }
        } else {
            node.right = insertHelper(node.right, key);
            
            // Maintain heap property
            if (node.right.priority > node.priority) {
                node = leftRotate(node);
            }
        }
        
        return node;
    }
    
    public boolean search(int key) {
        return searchHelper(root, key);
    }
    
    private boolean searchHelper(TreapNode node, int key) {
        if (node == null) {
            return false;
        }
        
        if (key == node.key) {
            return true;
        }
        
        if (key < node.key) {
            return searchHelper(node.left, key);
        } else {
            return searchHelper(node.right, key);
        }
    }
    
    public void delete(int key) {
        root = deleteHelper(root, key);
    }
    
    private TreapNode deleteHelper(TreapNode node, int key) {
        if (node == null) {
            return null;
        }
        
        if (key < node.key) {
            node.left = deleteHelper(node.left, key);
        } else if (key > node.key) {
            node.right = deleteHelper(node.right, key);
        } else {
            // Node to be deleted found
            if (node.left == null) {
                return node.right;
            } else if (node.right == null) {
                return node.left;
            } else {
                // Node has both children
                // Rotate the child with higher priority up
                if (node.left.priority > node.right.priority) {
                    node = rightRotate(node);
                    node.right = deleteHelper(node.right, key);
                } else {
                    node = leftRotate(node);
                    node.left = deleteHelper(node.left, key);
                }
            }
        }
        
        return node;
    }
    
    // Split treap into two parts: (<key) and (≥key)
    public TreapNode[] split(int key) {
        return splitHelper(root, key);
    }
    
    private TreapNode[] splitHelper(TreapNode node, int key) {
        if (node == null) {
            return new TreapNode[]{null, null};
        }
        
        if (key <= node.key) {
            TreapNode[] result = splitHelper(node.left, key);
            node.left = result[1];
            return new TreapNode[]{result[0], node};
        } else {
            TreapNode[] result = splitHelper(node.right, key);
            node.right = result[0];
            return new TreapNode[]{node, result[1]};
        }
    }
    
    // Merge two treaps (all keys in left < all keys in right)
    public static TreapNode merge(TreapNode left, TreapNode right) {
        if (left == null) return right;
        if (right == null) return left;
        
        if (left.priority > right.priority) {
            left.right = merge(left.right, right);
            return left;
        } else {
            right.left = merge(left, right.left);
            return right;
        }
    }
    
    // In-order traversal
    public void inorder() {
        inorderHelper(root);
        System.out.println();
    }
    
    private void inorderHelper(TreapNode node) {
        if (node != null) {
            inorderHelper(node.left);
            System.out.print(node.key + "(" + node.priority + ") ");
            inorderHelper(node.right);
        }
    }
    
    // Find minimum element
    public Integer findMin() {
        if (root == null) return null;
        TreapNode current = root;
        while (current.left != null) {
            current = current.left;
        }
        return current.key;
    }
    
    // Find maximum element
    public Integer findMax() {
        if (root == null) return null;
        TreapNode current = root;
        while (current.right != null) {
            current = current.right;
        }
        return current.key;
    }
}

// Using TreeSet as treap alternative for simpler operations
class TreapSimulation {
    private TreeSet<Integer> data;
    
    public TreapSimulation() {
        data = new TreeSet<>();
    }
    
    public void insert(int key) {
        data.add(key);
    }
    
    public boolean search(int key) {
        return data.contains(key);
    }
    
    public void delete(int key) {
        data.remove(key);
    }
    
    public NavigableSet<Integer> split(int key, boolean inclusive) {
        return inclusive ? data.tailSet(key, true) : data.tailSet(key, false);
    }
    
    public void merge(TreeSet<Integer> other) {
        data.addAll(other);
    }
    
    public String toString() {
        return data.toString();
    }
}

// Range query treap for counting elements in range
class RangeQueryTreap {
    private TreeSet<Integer> treap;
    
    public RangeQueryTreap() {
        treap = new TreeSet<>();
    }
    
    public void insert(int value) {
        treap.add(value);
    }
    
    public int countInRange(int low, int high) {
        return treap.subSet(low, true, high, true).size();
    }
    
    public List<Integer> getRange(int low, int high) {
        return new ArrayList<>(treap.subSet(low, true, high, true));
    }
    
    public Integer getKthSmallest(int k) {
        if (k <= 0 || k > treap.size()) return null;
        return treap.stream().skip(k - 1).findFirst().orElse(null);
    }
}

// Persistent treap implementation concept
class PersistentTreapNode {
    int key, priority;
    PersistentTreapNode left, right;
    
    public PersistentTreapNode(int key, int priority) {
        this.key = key;
        this.priority = priority;
    }
    
    // Copy constructor for path copying
    public PersistentTreapNode(PersistentTreapNode other) {
        this.key = other.key;
        this.priority = other.priority;
        this.left = other.left;
        this.right = other.right;
    }
}

// Usage examples
Treap treap = new Treap();
int[] values = {50, 30, 70, 20, 40, 60, 80};

System.out.println("Inserting values:");
for (int val : values) {
    treap.insert(val);
    System.out.print("After inserting " + val + ": ");
    treap.inorder();
}

System.out.println("Search 40: " + treap.search(40)); // true
System.out.println("Search 45: " + treap.search(45)); // false

System.out.println("Min: " + treap.findMin()); // 20
System.out.println("Max: " + treap.findMax()); // 80

System.out.println("Deleting 30:");
treap.delete(30);
treap.inorder();

// Split operation example
TreapNode[] split = treap.split(50);
System.out.println("Split at 50 - this creates two treaps");

// TreeSet simulation
TreapSimulation sim = new TreapSimulation();
for (int val : values) {
    sim.insert(val);
}
System.out.println("TreeSet simulation: " + sim);

// Range query example
RangeQueryTreap rangeTreeap = new RangeQueryTreap();
for (int i = 1; i <= 10; i++) {
    rangeTreeap.insert(i * 10);
}
System.out.println("Count in range [25, 75]: " + rangeTreeap.countInRange(25, 75));
System.out.println("3rd smallest: " + rangeTreeap.getKthSmallest(3));
```

## Python Snippet

```python
import random

class TreapNode:
    def __init__(self, key, pr=None):
        self.key = key; self.pr = random.randint(1, 10**9) if pr is None else pr
        self.left = None; self.right = None

def rotate_left(x):
    y = x.right; x.right = y.left; y.left = x; return y

def rotate_right(y):
    x = y.left; y.left = x.right; x.right = y; return x

def insert(root, key):
    if not root: return TreapNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
        if root.left.pr > root.pr: root = rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key)
        if root.right.pr > root.pr: root = rotate_left(root)
    return root

def search(root, key):
    while root and root.key != key:
        root = root.left if key < root.key else root.right
    return root is not None
```

## When to Use

- Simple randomized balanced BST implementation
- Persistent data structures with path copying
- Split and merge operations are frequent
- Alternative to complex rotation-based trees
- Cartesian tree applications

## Trade-offs

**Pros:**

- Simple implementation compared to red-black/AVL trees
- No complex balancing rules
- Natural split/merge operations
- Good expected performance
- Easy to make persistent

**Cons:**

- Randomized (not deterministic) performance
- Depends on good random number generator
- Can degenerate with bad luck
- Not widely used in standard libraries
- Worse constants than carefully tuned balanced trees

## Practice Problems

- **Merge k Sorted Lists**: Use treap for merging
- **Range Sum Query**: Augmented treap with subtree sums
- **Kth Smallest Element**: Order statistics with treap
- **Persistent Array**: Treap-based persistent structures
- **Interval Scheduling**: Split/merge for interval operations

<details>
<summary>Implementation Notes (Advanced)</summary>

### Randomization Properties

- **Expected height**: O(log n) with high probability
- **Priority assignment**: Random priorities ensure balance
- **Cartesian tree**: Treap is Cartesian tree of (key, priority) pairs
- **Uniqueness**: Structure determined by key-priority pairs

### Split and Merge Operations

- **Split complexity**: O(log n) expected time
- **Merge complexity**: O(log n) expected time
- **Applications**: Range operations, persistent structures
- **Invariant**: All keys in left < all keys in right for merge

### Persistent Implementations

- **Path copying**: Copy only nodes on path to root
- **Space complexity**: O(log n) per update
- **Functional programming**: Immutable tree structures
- **Garbage collection**: Old versions remain accessible

### Performance Optimization

- **Priority caching**: Precompute priorities for better locality
- **Iterative implementation**: Avoid recursion overhead
- **Memory pooling**: Reuse deleted nodes
- **Threaded trees**: Add threading for faster traversal

### Comparison with Alternatives

- **vs Red-Black**: Simpler code, worse constants
- **vs AVL**: Less strict balancing, easier split/merge  
- **vs Skip List**: Similar probabilistic guarantees
- **vs B-Trees**: Not optimized for disk I/O

</details>
