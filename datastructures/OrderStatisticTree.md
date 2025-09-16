# Order Statistic Tree

## Quick Definition

Augmented balanced binary search tree where each node maintains the size of its subtree. Enables efficient rank (position) and select (kth element) operations.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Select (kth) | **O(log n)** | — |
| Rank | **O(log n)** | — |

## Core Operations

```java
class OrderStatNode {
    int key;
    int size;  // size of subtree rooted at this node
    OrderStatNode left, right;
    
    public OrderStatNode(int key) {
        this.key = key;
        this.size = 1;
        this.left = this.right = null;
    }
}

class OrderStatisticTree {
    private OrderStatNode root;
    
    public OrderStatisticTree() {
        root = null;
    }
    
    // Update size of node based on children
    private void updateSize(OrderStatNode node) {
        if (node != null) {
            node.size = 1 + size(node.left) + size(node.right);
        }
    }
    
    // Get size of subtree (0 if null)
    private int size(OrderStatNode node) {
        return node == null ? 0 : node.size;
    }
    
    // Insert and maintain size information
    public void insert(int key) {
        root = insertHelper(root, key);
    }
    
    private OrderStatNode insertHelper(OrderStatNode node, int key) {
        if (node == null) {
            return new OrderStatNode(key);
        }
        
        if (key < node.key) {
            node.left = insertHelper(node.left, key);
        } else if (key > node.key) {
            node.right = insertHelper(node.right, key);
        } else {
            return node; // duplicate key
        }
        
        updateSize(node);
        return node; // In real implementation, add balancing here
    }
    
    // Find kth smallest element (1-indexed)
    public Integer select(int k) {
        return selectHelper(root, k);
    }
    
    private Integer selectHelper(OrderStatNode node, int k) {
        if (node == null) {
            return null;
        }
        
        int leftSize = size(node.left);
        
        if (k == leftSize + 1) {
            return node.key;
        } else if (k <= leftSize) {
            return selectHelper(node.left, k);
        } else {
            return selectHelper(node.right, k - leftSize - 1);
        }
    }
    
    // Find rank of element (1-indexed position in sorted order)
    public int rank(int key) {
        return rankHelper(root, key);
    }
    
    private int rankHelper(OrderStatNode node, int key) {
        if (node == null) {
            return 0;
        }
        
        if (key < node.key) {
            return rankHelper(node.left, key);
        } else if (key > node.key) {
            return size(node.left) + 1 + rankHelper(node.right, key);
        } else {
            return size(node.left) + 1;
        }
    }
    
    // Count elements in range [low, high]
    public int countRange(int low, int high) {
        return rank(high + 1) - rank(low);
    }
    
    // Get all elements in range [low, high]
    public List<Integer> rangeQuery(int low, int high) {
        List<Integer> result = new ArrayList<>();
        rangeQueryHelper(root, low, high, result);
        return result;
    }
    
    private void rangeQueryHelper(OrderStatNode node, int low, int high, List<Integer> result) {
        if (node == null) {
            return;
        }
        
        if (node.key >= low && node.key <= high) {
            rangeQueryHelper(node.left, low, high, result);
            result.add(node.key);
            rangeQueryHelper(node.right, low, high, result);
        } else if (node.key < low) {
            rangeQueryHelper(node.right, low, high, result);
        } else {
            rangeQueryHelper(node.left, low, high, result);
        }
    }
    
    // Get total number of elements
    public int size() {
        return size(root);
    }
    
    // Check if tree contains key
    public boolean contains(int key) {
        return rank(key) <= size() && select(rank(key)) == key;
    }
}

// Simpler implementation using ArrayList (for small datasets)
class ArrayOrderStatistics {
    private List<Integer> data;
    
    public ArrayOrderStatistics() {
        data = new ArrayList<>();
    }
    
    public void insert(int value) {
        int pos = Collections.binarySearch(data, value);
        if (pos < 0) {
            pos = -(pos + 1);
        }
        data.add(pos, value);
    }
    
    public Integer select(int k) {
        if (k <= 0 || k > data.size()) {
            return null;
        }
        return data.get(k - 1); // Convert to 0-indexed
    }
    
    public int rank(int value) {
        int pos = Collections.binarySearch(data, value);
        return pos >= 0 ? pos + 1 : -(pos + 1) + 1;
    }
    
    public int countRange(int low, int high) {
        return rank(high + 1) - rank(low);
    }
    
    public int size() {
        return data.size();
    }
}

// Using TreeSet for order statistics (Java Collections approach)
class TreeSetOrderStatistics {
    private TreeSet<Integer> set;
    
    public TreeSetOrderStatistics() {
        set = new TreeSet<>();
    }
    
    public void insert(int value) {
        set.add(value);
    }
    
    public Integer select(int k) {
        if (k <= 0 || k > set.size()) {
            return null;
        }
        return set.stream().skip(k - 1).findFirst().orElse(null);
    }
    
    public int rank(int value) {
        return set.headSet(value, false).size() + 1;
    }
    
    public int countRange(int low, int high) {
        return set.subSet(low, true, high, true).size();
    }
    
    public NavigableSet<Integer> rangeQuery(int low, int high) {
        return set.subSet(low, true, high, true);
    }
    
    public int size() {
        return set.size();
    }
}

// Rank tracking for competitive programming
class RankTracker {
    private TreeMap<Integer, Integer> scoreCount; // score -> count
    private int totalPlayers;
    
    public RankTracker() {
        scoreCount = new TreeMap<>();
        totalPlayers = 0;
    }
    
    public void addScore(int score) {
        scoreCount.merge(score, 1, Integer::sum);
        totalPlayers++;
    }
    
    public int getRank(int score) {
        int rank = 1;
        for (Map.Entry<Integer, Integer> entry : scoreCount.descendingMap().entrySet()) {
            if (entry.getKey() > score) {
                rank += entry.getValue();
            } else {
                break;
            }
        }
        return rank;
    }
    
    public Integer getScoreAtRank(int rank) {
        int count = 0;
        for (Map.Entry<Integer, Integer> entry : scoreCount.descendingMap().entrySet()) {
            count += entry.getValue();
            if (count >= rank) {
                return entry.getKey();
            }
        }
        return null;
    }
    
    public int getTotalPlayers() {
        return totalPlayers;
    }
}

// Usage examples
OrderStatisticTree ost = new OrderStatisticTree();
int[] values = {20, 8, 22, 4, 12, 10, 14};

System.out.println("Inserting values:");
for (int val : values) {
    ost.insert(val);
    System.out.println("After inserting " + val + ", size = " + ost.size());
}

System.out.println("\\nOrder statistics:");
System.out.println("1st smallest: " + ost.select(1));    // 4
System.out.println("3rd smallest: " + ost.select(3));    // 10
System.out.println("5th smallest: " + ost.select(5));    // 14

System.out.println("\\nRank queries:");
System.out.println("Rank of 10: " + ost.rank(10));       // 3
System.out.println("Rank of 14: " + ost.rank(14));       // 5
System.out.println("Rank of 25: " + ost.rank(25));       // 8 (would be inserted at end)

System.out.println("\\nRange queries:");
System.out.println("Count in range [8, 15]: " + ost.countRange(8, 15));  // 4 elements
System.out.println("Elements in range [8, 15]: " + ost.rangeQuery(8, 15));

// ArrayList approach for comparison
ArrayOrderStatistics aos = new ArrayOrderStatistics();
for (int val : values) {
    aos.insert(val);
}
System.out.println("\\nArrayList approach:");
System.out.println("3rd smallest: " + aos.select(3));
System.out.println("Rank of 12: " + aos.rank(12));

// TreeSet approach
TreeSetOrderStatistics tsos = new TreeSetOrderStatistics();
for (int val : values) {
    tsos.insert(val);
}
System.out.println("\\nTreeSet approach:");
System.out.println("2nd smallest: " + tsos.select(2));
System.out.println("Range [10, 20]: " + tsos.rangeQuery(10, 20));

// Rank tracker example
RankTracker tracker = new RankTracker();
int[] scores = {95, 87, 92, 87, 98, 85};
for (int score : scores) {
    tracker.addScore(score);
}
System.out.println("\\nRank tracker:");
System.out.println("Rank of score 92: " + tracker.getRank(92));
System.out.println("Score at rank 2: " + tracker.getScoreAtRank(2));
```

## Python Snippet

```python
class Node:
    def __init__(self, key):
        self.key = key; self.left = None; self.right = None; self.size = 1

def size(n): return n.size if n else 0
def upd(n):
    if n: n.size = 1 + size(n.left) + size(n.right)

def insert(root, key):
    if not root: return Node(key)
    if key < root.key: root.left = insert(root.left, key)
    elif key > root.key: root.right = insert(root.right, key)
    upd(root); return root

def select(root, k):  # 1-indexed
    if not root: return None
    ls = size(root.left)
    if k == ls + 1: return root.key
    if k <= ls: return select(root.left, k)
    return select(root.right, k - ls - 1)

def rank(root, key):  # 1-indexed position
    if not root: return 0
    if key < root.key: return rank(root.left, key)
    if key > root.key: return size(root.left) + 1 + rank(root.right, key)
    return size(root.left) + 1

def count_range(root, low, high):
    return rank(root, high + 1) - rank(root, low)
```

## When to Use

- Dynamic ranking and leaderboard systems
- Quantile and percentile calculations
- Range counting queries
- Order statistics in streaming data
- Competitive programming problems

## Trade-offs

**Pros:**

- Efficient kth element and rank queries
- Dynamic insertion and deletion
- Range counting in O(log n)
- Useful for many algorithmic problems
- Can be built on existing balanced trees

**Cons:**

- Additional space overhead for size information
- More complex implementation
- Not available in standard libraries
- Requires balanced tree for good performance

## Practice Problems

- **Kth Largest Element in Array**: Order statistics on dynamic data
- **Count of Smaller Numbers**: Rank-based counting
- **Range Sum Query**: With coordinate compression
- **Median from Data Stream**: Dynamic median with order statistics
- **Meeting Rooms**: Interval scheduling with order statistics

<details>
<summary>Implementation Notes (Advanced)</summary>

### Augmentation Strategy

- **Size maintenance**: Update subtree sizes during tree operations
- **Invariant**: node.size = 1 + node.left.size + node.right.size
- **Balancing**: Must maintain balance while preserving size information
- **Rotation updates**: Size changes during tree rotations

### Tree Balancing

- **Red-Black Tree**: Can be augmented with size information
- **AVL Tree**: Height and size can be maintained together
- **Treap**: Size maintenance with randomized balancing
- **Splay Tree**: Size information with self-adjusting property

### Alternative Implementations

- **Fenwick Tree**: For prefix sum-based order statistics
- **Segment Tree**: Range-based order statistics
- **Skip List**: Probabilistic order statistics
- **B-Trees**: External memory order statistics

### Performance Optimization

- **Cache-friendly**: Consider memory layout for better locality
- **Lazy propagation**: For range updates with order statistics
- **Persistent versions**: Functional order statistic trees
- **Parallel algorithms**: Concurrent order statistic operations

### Applications

- **Database indexing**: Order statistics for SQL queries
- **Statistical analysis**: Quantile computation
- **Game rankings**: Real-time leaderboards
- **Financial systems**: Order book analysis

</details>
