# B-Tree

## Quick Definition

Self-balancing multi-way search tree designed for efficient disk I/O. Each node can have multiple keys and children, minimizing tree height for databases and file systems.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Range Scan | O(log n + k) | — |

## Core Operations

```java
class BTreeNode {
    int t; // minimum degree (defines the range for number of keys)
    List<Integer> keys;
    List<BTreeNode> children;
    boolean isLeaf;
    
    public BTreeNode(int t, boolean isLeaf) {
        this.t = t;
        this.keys = new ArrayList<>();
        this.children = new ArrayList<>();
        this.isLeaf = isLeaf;
    }
    
    // Search for a key in this node
    public boolean search(int key) {
        int i = 0;
        while (i < keys.size() && key > keys.get(i)) {
            i++;
        }
        
        if (i < keys.size() && key == keys.get(i)) {
            return true;
        }
        
        if (isLeaf) {
            return false;
        }
        
        return children.get(i).search(key);
    }
    
    // Insert a key into a non-full node
    public void insertNonFull(int key) {
        int i = keys.size() - 1;
        
        if (isLeaf) {
            keys.add(0);  // placeholder
            while (i >= 0 && keys.get(i) > key) {
                keys.set(i + 1, keys.get(i));
                i--;
            }
            keys.set(i + 1, key);
        } else {
            while (i >= 0 && keys.get(i) > key) {
                i--;
            }
            i++;
            
            if (children.get(i).keys.size() == 2 * t - 1) {
                splitChild(i);
                if (keys.get(i) < key) {
                    i++;
                }
            }
            children.get(i).insertNonFull(key);
        }
    }
    
    // Split a full child
    public void splitChild(int i) {
        BTreeNode fullChild = children.get(i);
        BTreeNode newChild = new BTreeNode(t, fullChild.isLeaf);
        
        // Move the last (t-1) keys of fullChild to newChild
        for (int j = 0; j < t - 1; j++) {
            newChild.keys.add(fullChild.keys.get(j + t));
        }
        
        // Move the last t children of fullChild to newChild
        if (!fullChild.isLeaf) {
            for (int j = 0; j < t; j++) {
                newChild.children.add(fullChild.children.get(j + t));
            }
        }
        
        // Insert newChild as a child of this node
        children.add(i + 1, newChild);
        
        // Move the middle key of fullChild up to this node
        keys.add(i, fullChild.keys.get(t - 1));
        
        // Trim fullChild
        fullChild.keys = new ArrayList<>(fullChild.keys.subList(0, t - 1));
        if (!fullChild.isLeaf) {
            fullChild.children = new ArrayList<>(fullChild.children.subList(0, t));
        }
    }
    
    // In-order traversal
    public void traverse() {
        int i;
        for (i = 0; i < keys.size(); i++) {
            if (!isLeaf) {
                children.get(i).traverse();
            }
            System.out.print(keys.get(i) + " ");
        }
        
        if (!isLeaf) {
            children.get(i).traverse();
        }
    }
}

class BTree {
    private BTreeNode root;
    private int t; // minimum degree
    
    public BTree(int t) {
        this.t = t;
        this.root = new BTreeNode(t, true);
    }
    
    public boolean search(int key) {
        return root.search(key);
    }
    
    public void insert(int key) {
        if (root.keys.size() == 2 * t - 1) {
            BTreeNode newRoot = new BTreeNode(t, false);
            newRoot.children.add(root);
            newRoot.splitChild(0);
            root = newRoot;
        }
        root.insertNonFull(key);
    }
    
    public void traverse() {
        if (root != null) {
            root.traverse();
        }
    }
    
    public void printTree() {
        if (root != null) {
            printTreeHelper(root, 0);
        }
    }
    
    private void printTreeHelper(BTreeNode node, int level) {
        System.out.print("Level " + level + ": ");
        for (int key : node.keys) {
            System.out.print(key + " ");
        }
        System.out.println();
        
        if (!node.isLeaf) {
            for (BTreeNode child : node.children) {
                printTreeHelper(child, level + 1);
            }
        }
    }
}

// Simplified B-Tree simulation using TreeSet for ordering
class BTreeSimulation {
    private TreeSet<Integer> data;
    private int degree;
    
    public BTreeSimulation(int degree) {
        this.degree = degree;
        this.data = new TreeSet<>();
    }
    
    public void insert(int key) {
        data.add(key);
    }
    
    public boolean search(int key) {
        return data.contains(key);
    }
    
    public List<Integer> rangeQuery(int min, int max) {
        return new ArrayList<>(data.subSet(min, true, max, true));
    }
    
    public void printStructure() {
        System.out.println("B-Tree contents: " + data);
    }
}

// Database index simulation
class DatabaseIndex {
    private TreeMap<Integer, String> index;
    
    public DatabaseIndex() {
        this.index = new TreeMap<>();
    }
    
    public void createIndex(int id, String record) {
        index.put(id, record);
    }
    
    public String lookup(int id) {
        return index.get(id);
    }
    
    public List<String> rangeQuery(int startId, int endId) {
        return new ArrayList<>(index.subMap(startId, true, endId, true).values());
    }
    
    public void bulkLoad(Map<Integer, String> records) {
        index.putAll(records);
    }
}

// Usage examples
BTree btree = new BTree(3); // minimum degree = 3
int[] values = {10, 20, 5, 6, 12, 30, 7, 17};

for (int val : values) {
    btree.insert(val);
}

System.out.println("B-Tree traversal:");
btree.traverse();  // prints in sorted order

System.out.println("\nSearch 6: " + btree.search(6));   // true
System.out.println("Search 15: " + btree.search(15)); // false

System.out.println("\nTree structure:");
btree.printTree();

// Database simulation
DatabaseIndex dbIndex = new DatabaseIndex();
dbIndex.createIndex(1001, "Alice");
dbIndex.createIndex(1005, "Bob");
dbIndex.createIndex(1003, "Charlie");
dbIndex.createIndex(1007, "David");

System.out.println("Lookup 1003: " + dbIndex.lookup(1003)); // Charlie
System.out.println("Range [1002, 1006]: " + dbIndex.rangeQuery(1002, 1006));
```

## Python Snippet

```python
class BTreeNode:
    def __init__(self, t, is_leaf):
        self.t = t; self.leaf = is_leaf
        self.keys = []
        self.children = []

    def search(self, k):
        i = 0
        while i < len(self.keys) and k > self.keys[i]: i += 1
        if i < len(self.keys) and self.keys[i] == k: return True
        if self.leaf: return False
        return self.children[i].search(k)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t:]
        if not y.leaf:
            z.children = y.children[t:]
        self.children.insert(i+1, z)
        self.keys.insert(i, y.keys[t-1])
        y.keys = y.keys[:t-1]
        if not y.leaf:
            y.children = y.children[:t]

    def insert_non_full(self, k):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(0)
            while i >= 0 and self.keys[i] > k:
                self.keys[i+1] = self.keys[i]; i -= 1
            self.keys[i+1] = k
        else:
            while i >= 0 and self.keys[i] > k: i -= 1
            i += 1
            if len(self.children[i].keys) == 2*self.t - 1:
                self.split_child(i)
                if self.keys[i] < k: i += 1
            self.children[i].insert_non_full(k)

class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, True)
    def search(self, k):
        return self.root.search(k)
    def insert(self, k):
        r = self.root
        if len(r.keys) == 2*self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.append(r)
            s.split_child(0)
            self.root = s
            idx = 0 if k < s.keys[0] else 1
            s.children[idx].insert_non_full(k)
        else:
            r.insert_non_full(k)
```

## When to Use

- Database storage engines and indexes
- File system directory structures
- External sorting with limited memory
- Applications requiring efficient disk I/O
- Large datasets that don't fit in memory

## Trade-offs

**Pros:**

- Optimized for disk I/O operations
- Logarithmic height with high fanout
- Excellent range query performance
- Self-balancing maintains performance
- Cache-friendly sequential access

**Cons:**

- Complex implementation compared to binary trees
- Higher memory overhead per node
- More complex deletion algorithm
- Not ideal for small datasets in memory

## Practice Problems

- **Design B-Tree**: Implement insert with splitting
- **Range Sum Query**: Use B-Tree for large datasets
- **Database Storage Engine**: Design with B-Tree indexing
- **File System Directory**: Implement directory structure
- **External Sorting**: Merge using B-Tree principles

<details>
<summary>Implementation Notes (Advanced)</summary>

### Node Structure Design

- **Minimum degree t**: Node contains [t-1, 2t-1] keys
- **Children count**: Internal nodes have [t, 2t] children
- **Leaf nodes**: Contain only keys, no children
- **Full nodes**: Contain exactly 2t-1 keys (must split)

### Disk I/O Optimization

- **Node size**: Usually matches disk block size (4KB, 8KB)
- **Sequential access**: Range queries benefit from locality
- **Buffering**: Cache frequently accessed nodes
- **Write-ahead logging**: For crash recovery

### B-Tree Variants

- **B+ Tree**: All data in leaves, internal nodes only for navigation
- **B* Tree**: Delayed splitting, higher utilization
- **Counted B-Tree**: Maintains subtree sizes for order statistics
- **Concurrent B-Tree**: Lock-coupling for multi-threading

### Performance Characteristics

- **Height**: O(log_t n) where t is minimum degree
- **Disk accesses**: Proportional to tree height
- **Node utilization**: Guaranteed at least 50% full
- **Range queries**: Efficient due to ordered structure

### Implementation Considerations

- **Memory management**: Handle large nodes efficiently
- **Serialization**: Convert nodes to/from disk format
- **Concurrency**: Multiple readers, exclusive writers
- **Recovery**: Transaction logging and rollback

</details>
