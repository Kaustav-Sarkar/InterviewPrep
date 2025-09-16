# B+ Tree

## Quick Definition

Balanced multi-way tree where all data is stored in leaf nodes, with internal nodes containing only keys for navigation. Optimized for database systems and file storage with excellent range query performance.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Range Query | O(log n + k) | — |

*k = number of results in range*

## Core Operations

```java
class BPlusTreeNode {
    boolean isLeaf;
    int degree;
    List<Integer> keys;
    List<BPlusTreeNode> children; // for internal nodes
    List<String> values; // for leaf nodes
    BPlusTreeNode next; // leaf node linked list
    
    public BPlusTreeNode(int degree, boolean isLeaf) {
        this.degree = degree;
        this.isLeaf = isLeaf;
        this.keys = new ArrayList<>();
        
        if (isLeaf) {
            this.values = new ArrayList<>();
        } else {
            this.children = new ArrayList<>();
        }
    }
}

class BPlusTree {
    private BPlusTreeNode root;
    private int degree;
    
    public BPlusTree(int degree) {
        this.degree = degree;
        this.root = new BPlusTreeNode(degree, true);
    }
    
    // Search for a key
    public String search(int key) {
        return searchHelper(root, key);
    }
    
    private String searchHelper(BPlusTreeNode node, int key) {
        if (node.isLeaf) {
            for (int i = 0; i < node.keys.size(); i++) {
                if (node.keys.get(i) == key) {
                    return node.values.get(i);
                }
            }
            return null;
        }
        
        int i = 0;
        while (i < node.keys.size() && key >= node.keys.get(i)) {
            i++;
        }
        return searchHelper(node.children.get(i), key);
    }
    
    // Range query - efficient with linked leaves
    public List<Map.Entry<Integer, String>> rangeQuery(int startKey, int endKey) {
        List<Map.Entry<Integer, String>> result = new ArrayList<>();
        BPlusTreeNode leaf = findLeaf(startKey);
        
        while (leaf != null) {
            for (int i = 0; i < leaf.keys.size(); i++) {
                int key = leaf.keys.get(i);
                if (key >= startKey && key <= endKey) {
                    result.add(new AbstractMap.SimpleEntry<>(key, leaf.values.get(i)));
                } else if (key > endKey) {
                    return result;
                }
            }
            leaf = leaf.next;
        }
        return result;
    }
}

// Usage example with TreeMap comparison
BPlusTree bplus = new BPlusTree(4);
TreeMap<Integer, String> treemap = new TreeMap<>();

// Insert data
bplus.insert(10, "Alice");
bplus.insert(20, "Bob");
bplus.insert(15, "Charlie");

// Range queries
List<Map.Entry<Integer, String>> range = bplus.rangeQuery(10, 20);
NavigableMap<Integer, String> treeRange = treemap.subMap(10, true, 20, true);
```

## Python Snippet

```python
class BPlusNode:
    def __init__(self, degree, leaf=False):
        self.leaf = leaf; self.degree = degree
        self.keys = []
        self.children = []  # for internal: child pointers; for leaf: values
        self.next = None    # leaf linkage

def find_leaf(root, key):
    node = root
    while not node.leaf:
        i = 0
        while i < len(node.keys) and key >= node.keys[i]: i += 1
        node = node.children[i]
    return node

def range_query(root, lo, hi):
    leaf = find_leaf(root, lo)
    res = []
    while leaf:
        for k, v in zip(leaf.keys, leaf.children):
            if lo <= k <= hi: res.append((k, v))
            if k > hi: return res
        leaf = leaf.next
    return res
```

## When to Use

- Database storage engines and indexing
- File systems requiring fast range queries
- Large datasets with frequent range scans
- Systems optimized for disk I/O patterns
- Applications needing sorted data access

## Trade-offs

**Pros:**

- Excellent range query performance
- All data in leaves enables efficient scans
- Optimal for disk-based storage systems
- High fanout reduces tree height
- Linked leaves provide sequential access

**Cons:**

- More complex than regular B-Trees
- Higher space overhead than binary trees
- Requires careful tuning of degree parameter
- Implementation complexity for deletion
- Not ideal for small datasets in memory

## Practice Problems

- **Design Database Index**: Implement B+ tree for table indexing
- **Range Sum Query**: Use B+ tree for efficient range sums
- **File System**: Directory structure with fast lookups
- **Time Series Data**: Efficient range queries by timestamp
- **Log Analysis**: Query logs within time ranges

<details>
<summary>Implementation Notes (Advanced)</summary>

### B+ Tree vs B-Tree Differences

- **Data location**: B+ trees store all data in leaves only
- **Internal nodes**: Contain only keys for navigation
- **Leaf linking**: Leaves form a linked list for range scans
- **Key duplication**: Keys appear in both internal and leaf nodes

### Node Design

- **Leaf nodes**: Store key-value pairs + next pointer
- **Internal nodes**: Store keys + child pointers
- **Degree selection**: Usually matches disk block size
- **Fanout**: High fanout reduces tree height

### Range Query Optimization

- **Sequential access**: Linked leaves enable efficient scans
- **Minimal disk I/O**: Range queries touch fewer nodes
- **Buffering**: Can prefetch sequential leaf pages
- **Index-only scans**: Some queries satisfied by internal nodes only

### Disk Storage Optimization

- **Page size**: Nodes sized to match disk pages
- **Clustering**: Store related data together
- **Compression**: Key compression for better fanout
- **Caching**: Buffer frequently accessed nodes

</details>
