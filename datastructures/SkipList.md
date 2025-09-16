# Skip List

## Quick Definition

Probabilistic data structure with multiple levels of linked lists. Uses randomization to maintain balance and provides expected O(log n) operations without rotations.

## Big-O Summary

| Operation | Time (Expected) | Space |
|-----------|----------------|-------|
| Search | **O(log n)** | O(n) |
| Insert | **O(log n)** | — |
| Delete | **O(log n)** | — |
| Range Query | O(log n + k) | — |

## Core Operations

```java
class SkipListNode {
    int value;
    SkipListNode[] forward;  // array of forward pointers
    
    public SkipListNode(int value, int level) {
        this.value = value;
        this.forward = new SkipListNode[level + 1];
    }
}

class SkipList {
    private static final int MAX_LEVEL = 16;
    private static final double P = 0.5;  // probability factor
    
    private SkipListNode header;
    private int currentLevel;
    private Random random;
    
    public SkipList() {
        header = new SkipListNode(Integer.MIN_VALUE, MAX_LEVEL);
        currentLevel = 0;
        random = new Random();
    }
    
    private int randomLevel() {
        int level = 0;
        while (random.nextDouble() < P && level < MAX_LEVEL) {
            level++;
        }
        return level;
    }
    
    public boolean search(int target) {
        SkipListNode current = header;
        
        // Start from highest level and work down
        for (int i = currentLevel; i >= 0; i--) {
            while (current.forward[i] != null && current.forward[i].value < target) {
                current = current.forward[i];
            }
        }
        
        current = current.forward[0];
        return current != null && current.value == target;
    }
    
    public void insert(int value) {
        SkipListNode[] update = new SkipListNode[MAX_LEVEL + 1];
        SkipListNode current = header;
        
        // Find insertion position
        for (int i = currentLevel; i >= 0; i--) {
            while (current.forward[i] != null && current.forward[i].value < value) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        // Don't insert duplicate
        if (current != null && current.value == value) {
            return;
        }
        
        // Generate random level for new node
        int newLevel = randomLevel();
        
        if (newLevel > currentLevel) {
            for (int i = currentLevel + 1; i <= newLevel; i++) {
                update[i] = header;
            }
            currentLevel = newLevel;
        }
        
        // Create new node and update pointers
        SkipListNode newNode = new SkipListNode(value, newLevel);
        for (int i = 0; i <= newLevel; i++) {
            newNode.forward[i] = update[i].forward[i];
            update[i].forward[i] = newNode;
        }
    }
    
    public boolean delete(int value) {
        SkipListNode[] update = new SkipListNode[MAX_LEVEL + 1];
        SkipListNode current = header;
        
        // Find deletion position
        for (int i = currentLevel; i >= 0; i--) {
            while (current.forward[i] != null && current.forward[i].value < value) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        if (current == null || current.value != value) {
            return false;  // value not found
        }
        
        // Update pointers to skip deleted node
        for (int i = 0; i <= currentLevel; i++) {
            if (update[i].forward[i] != current) {
                break;
            }
            update[i].forward[i] = current.forward[i];
        }
        
        // Update current level
        while (currentLevel > 0 && header.forward[currentLevel] == null) {
            currentLevel--;
        }
        
        return true;
    }
}

// Simplified skip list using Java's ConcurrentSkipListSet
ConcurrentSkipListSet<Integer> skipSet = new ConcurrentSkipListSet<>();

// Basic operations
skipSet.add(10); skipSet.add(5); skipSet.add(15);
skipSet.add(20); skipSet.add(8);

System.out.println("Contains 10: " + skipSet.contains(10)); // true
System.out.println("First: " + skipSet.first());             // 5
System.out.println("Last: " + skipSet.last());               // 20

// Range operations
System.out.println("Lower than 12: " + skipSet.lower(12));   // 10
System.out.println("Floor of 12: " + skipSet.floor(12));     // 10
System.out.println("Ceiling of 12: " + skipSet.ceiling(12)); // 15

// Subset operations
System.out.println("Subset [8, 15]: " + skipSet.subSet(8, true, 15, true));

// ConcurrentSkipListMap for key-value pairs
ConcurrentSkipListMap<Integer, String> skipMap = new ConcurrentSkipListMap<>();
skipMap.put(10, "ten");
skipMap.put(5, "five");
skipMap.put(15, "fifteen");

// Usage examples
SkipList skipList = new SkipList();
skipList.insert(3); skipList.insert(6); skipList.insert(7);
skipList.insert(9); skipList.insert(12); skipList.insert(19);

System.out.println("Search 7: " + skipList.search(7));     // true
System.out.println("Search 5: " + skipList.search(5));     // false

skipList.delete(7);
System.out.println("Search 7 after delete: " + skipList.search(7)); // false
```

## Python Snippet

```python
import random

MAX_LEVEL = 16; P = 0.5

class Node:
    def __init__(self, val, level):
        self.val = val; self.forward = [None]*(level+1)

class SkipList:
    def __init__(self):
        self.head = Node(float('-inf'), MAX_LEVEL); self.level = 0
    def _rand_level(self):
        lvl = 0
        while random.random() < P and lvl < MAX_LEVEL: lvl += 1
        return lvl
    def search(self, target):
        cur = self.head
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < target:
                cur = cur.forward[i]
        cur = cur.forward[0]
        return cur is not None and cur.val == target
    def insert(self, val):
        update = [None]*(MAX_LEVEL+1); cur = self.head
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
            update[i] = cur
        cur = cur.forward[0]
        if cur and cur.val == val: return
        lvl = self._rand_level()
        if lvl > self.level:
            for i in range(self.level+1, lvl+1): update[i] = self.head
            self.level = lvl
        node = Node(val, lvl)
        for i in range(lvl+1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
    def delete(self, val):
        update = [None]*(MAX_LEVEL+1); cur = self.head
        for i in range(self.level, -1, -1):
            while cur.forward[i] and cur.forward[i].val < val:
                cur = cur.forward[i]
            update[i] = cur
        cur = cur.forward[0]
        if not cur or cur.val != val: return False
        for i in range(self.level+1):
            if update[i].forward[i] != cur: break
            update[i].forward[i] = cur.forward[i]
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        return True
```

## When to Use

- Concurrent data structures (ConcurrentSkipListMap/Set)
- Real-time systems requiring predictable performance
- Range queries on ordered data
- Alternative to balanced trees with simpler implementation
- Lock-free concurrent algorithms

## Trade-offs

**Pros:**

- Simple implementation compared to balanced trees
- Good concurrent performance
- No rebalancing required
- Expected O(log n) operations
- Lock-free implementations possible

**Cons:**

- Probabilistic guarantees (not deterministic)
- Extra memory for forward pointers
- Worst-case O(n) operations possible
- Cache performance worse than arrays

## Practice Problems

- **Design Skiplist**: Implement search, insert, delete
- **Range Sum Query**: Use skip list for efficient range operations
- **Closest Elements**: Find k closest elements to target
- **Time-based Key-Value Store**: Skip list with timestamps
- **Leaderboard System**: Maintain sorted scores

<details>
<summary>Implementation Notes (Advanced)</summary>

### Probabilistic Analysis

- **Expected height**: O(log n) with probability 1/2
- **Level distribution**: Geometric distribution with parameter p
- **Space complexity**: Expected O(n) with constant factor
- **Search path**: Expected O(log n) comparisons

### Parameter Tuning

- **Probability p**: Usually 1/2 or 1/4
- **Maximum level**: log₂(n) or fixed constant
- **Level generation**: Geometric random variable
- **Performance trade-offs**: Space vs time

### Concurrent Implementation

- **Lock-free algorithms**: Use atomic operations
- **Memory ordering**: Careful ordering of pointer updates
- **Thread safety**: ConcurrentSkipListMap provides this

### Optimization Techniques

- **Finger search**: Start from previous position
- **Bulk loading**: Build skip list from sorted data
- **Adaptive levels**: Adjust based on data distribution

</details>
