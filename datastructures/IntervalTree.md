# Interval Tree

## Quick Definition

Balanced binary search tree where each node stores an interval and maintains maximum endpoint in subtree. Efficiently finds all intervals overlapping with a query.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Insert | **O(log n)** | O(n) |
| Delete | **O(log n)** | — |
| Search Overlap | **O(log n + k)** | — |
| Point Query | O(log n + k) | — |

*k = number of overlapping intervals*

## Core Operations

```java
class Interval {
    int start, end;
    
    public Interval(int start, int end) {
        this.start = start;
        this.end = end;
    }
    
    public boolean overlaps(Interval other) {
        return this.start <= other.end && other.start <= this.end;
    }
    
    public boolean overlaps(int point) {
        return this.start <= point && point <= this.end;
    }
    
    @Override
    public String toString() {
        return "[" + start + ", " + end + "]";
    }
}

class IntervalNode {
    Interval interval;
    int maxEnd;  // maximum end point in this subtree
    IntervalNode left, right;
    
    public IntervalNode(Interval interval) {
        this.interval = interval;
        this.maxEnd = interval.end;
        this.left = this.right = null;
    }
}

class IntervalTree {
    private IntervalNode root;
    
    public void insert(Interval interval) {
        root = insertHelper(root, interval);
    }
    
    private IntervalNode insertHelper(IntervalNode node, Interval interval) {
        // Base case: create new node
        if (node == null) {
            return new IntervalNode(interval);
        }
        
        // Insert based on start time
        if (interval.start < node.interval.start) {
            node.left = insertHelper(node.left, interval);
        } else {
            node.right = insertHelper(node.right, interval);
        }
        
        // Update maxEnd
        node.maxEnd = Math.max(node.maxEnd, interval.end);
        
        return node;
    }
    
    // Find any interval that overlaps with given interval
    public Interval searchOverlap(Interval queryInterval) {
        return searchOverlapHelper(root, queryInterval);
    }
    
    private Interval searchOverlapHelper(IntervalNode node, Interval queryInterval) {
        if (node == null) {
            return null;
        }
        
        // Check if current interval overlaps
        if (node.interval.overlaps(queryInterval)) {
            return node.interval;
        }
        
        // If left subtree has potential overlap, search left
        if (node.left != null && node.left.maxEnd >= queryInterval.start) {
            return searchOverlapHelper(node.left, queryInterval);
        }
        
        // Otherwise search right
        return searchOverlapHelper(node.right, queryInterval);
    }
    
    // Find all intervals that overlap with given interval
    public List<Interval> findAllOverlaps(Interval queryInterval) {
        List<Interval> result = new ArrayList<>();
        findAllOverlapsHelper(root, queryInterval, result);
        return result;
    }
    
    private void findAllOverlapsHelper(IntervalNode node, Interval queryInterval, List<Interval> result) {
        if (node == null) {
            return;
        }
        
        // Check current interval
        if (node.interval.overlaps(queryInterval)) {
            result.add(node.interval);
        }
        
        // Search left subtree if it can have overlaps
        if (node.left != null && node.left.maxEnd >= queryInterval.start) {
            findAllOverlapsHelper(node.left, queryInterval, result);
        }
        
        // Search right subtree if current node's start is within query
        if (node.right != null && node.interval.start <= queryInterval.end) {
            findAllOverlapsHelper(node.right, queryInterval, result);
        }
    }
    
    // Find all intervals containing a point
    public List<Interval> findIntervalsContaining(int point) {
        List<Interval> result = new ArrayList<>();
        findPointHelper(root, point, result);
        return result;
    }
    
    private void findPointHelper(IntervalNode node, int point, List<Interval> result) {
        if (node == null) {
            return;
        }
        
        // Check if current interval contains the point
        if (node.interval.overlaps(point)) {
            result.add(node.interval);
        }
        
        // Search left if left subtree can contain the point
        if (node.left != null && node.left.maxEnd >= point) {
            findPointHelper(node.left, point, result);
        }
        
        // Search right if point is >= current start
        if (node.right != null && point >= node.interval.start) {
            findPointHelper(node.right, point, result);
        }
    }
    
    // In-order traversal for debugging
    public void inorder() {
        inorderHelper(root);
    }
    
    private void inorderHelper(IntervalNode node) {
        if (node != null) {
            inorderHelper(node.left);
            System.out.print(node.interval + "(max:" + node.maxEnd + ") ");
            inorderHelper(node.right);
        }
    }
}

// Calendar booking system using interval tree
class CalendarBooking {
    private IntervalTree intervalTree;
    private List<Interval> bookings;
    
    public CalendarBooking() {
        intervalTree = new IntervalTree();
        bookings = new ArrayList<>();
    }
    
    public boolean book(int start, int end) {
        Interval newInterval = new Interval(start, end - 1); // exclusive end
        
        // Check for conflicts
        Interval conflict = intervalTree.searchOverlap(newInterval);
        if (conflict != null) {
            return false; // Booking conflict
        }
        
        // No conflict, add the booking
        intervalTree.insert(newInterval);
        bookings.add(newInterval);
        return true;
    }
    
    public List<Interval> getBookingsAt(int time) {
        return intervalTree.findIntervalsContaining(time);
    }
    
    public List<Interval> getAllBookings() {
        return new ArrayList<>(bookings);
    }
}

// Meeting room scheduler
class MeetingRoomScheduler {
    private IntervalTree roomSchedule;
    
    public MeetingRoomScheduler() {
        roomSchedule = new IntervalTree();
    }
    
    public boolean scheduleRoom(int startTime, int endTime) {
        Interval meeting = new Interval(startTime, endTime - 1);
        
        // Check if room is available
        if (roomSchedule.searchOverlap(meeting) != null) {
            return false; // Room not available
        }
        
        roomSchedule.insert(meeting);
        return true;
    }
    
    public List<Interval> getConflicts(int startTime, int endTime) {
        Interval query = new Interval(startTime, endTime - 1);
        return roomSchedule.findAllOverlaps(query);
    }
    
    public boolean isRoomFree(int time) {
        return roomSchedule.findIntervalsContaining(time).isEmpty();
    }
}

// Using TreeMap for simpler interval operations
class SimpleIntervalScheduler {
    private TreeMap<Integer, Integer> schedule; // start -> end mapping
    
    public SimpleIntervalScheduler() {
        schedule = new TreeMap<>();
    }
    
    public boolean addEvent(int start, int end) {
        // Check for overlap with existing events
        Map.Entry<Integer, Integer> floor = schedule.floorEntry(start);
        Map.Entry<Integer, Integer> ceiling = schedule.ceilingEntry(start);
        
        // Check if overlaps with previous event
        if (floor != null && floor.getValue() > start) {
            return false;
        }
        
        // Check if overlaps with next event
        if (ceiling != null && ceiling.getKey() < end) {
            return false;
        }
        
        schedule.put(start, end);
        return true;
    }
    
    public List<int[]> getEventsInRange(int queryStart, int queryEnd) {
        List<int[]> result = new ArrayList<>();
        
        for (Map.Entry<Integer, Integer> entry : schedule.entrySet()) {
            int start = entry.getKey();
            int end = entry.getValue();
            
            // Check for overlap
            if (start < queryEnd && end > queryStart) {
                result.add(new int[]{start, end});
            }
        }
        
        return result;
    }
}

// Usage examples
IntervalTree tree = new IntervalTree();

// Insert intervals
tree.insert(new Interval(15, 20));
tree.insert(new Interval(10, 30));
tree.insert(new Interval(17, 19));
tree.insert(new Interval(5, 20));
tree.insert(new Interval(12, 15));
tree.insert(new Interval(30, 40));

System.out.println("Tree structure:");
tree.inorder();

// Search for overlaps
Interval query = new Interval(14, 16);
System.out.println("\nOverlap with [14, 16]: " + tree.searchOverlap(query));

List<Interval> allOverlaps = tree.findAllOverlaps(query);
System.out.println("All overlaps with [14, 16]: " + allOverlaps);

// Point query
List<Interval> containing18 = tree.findIntervalsContaining(18);
System.out.println("Intervals containing point 18: " + containing18);

// Calendar booking example
CalendarBooking calendar = new CalendarBooking();
System.out.println("Book [10, 15): " + calendar.book(10, 15)); // true
System.out.println("Book [12, 17): " + calendar.book(12, 17)); // false (conflict)
System.out.println("Book [16, 20): " + calendar.book(16, 20)); // true
```

## Python Snippet

```python
class Interval:
    def __init__(self, start, end):
        self.start, self.end = start, end
    def overlaps_iv(self, other):
        return self.start <= other.end and other.start <= self.end
    def overlaps_pt(self, p):
        return self.start <= p <= self.end
    def __repr__(self):
        return f"[{self.start}, {self.end}]"

class IntervalNode:
    def __init__(self, iv):
        self.iv = iv; self.maxEnd = iv.end; self.left = None; self.right = None

class IntervalTree:
    def __init__(self):
        self.root = None
    def insert(self, iv):
        self.root = self._ins(self.root, iv)
    def _ins(self, node, iv):
        if not node: return IntervalNode(iv)
        if iv.start < node.iv.start:
            node.left = self._ins(node.left, iv)
        else:
            node.right = self._ins(node.right, iv)
        node.maxEnd = max(node.maxEnd, iv.end)
        return node
    def search_overlap(self, q):
        node = self.root
        while node:
            if node.iv.overlaps_iv(q): return node.iv
            if node.left and node.left.maxEnd >= q.start:
                node = node.left
            else:
                node = node.right
        return None
    def find_all_overlaps(self, q):
        res = []
        def dfs(n):
            if not n: return
            if n.iv.overlaps_iv(q): res.append(n.iv)
            if n.left and n.left.maxEnd >= q.start: dfs(n.left)
            if n.right and n.iv.start <= q.end: dfs(n.right)
        dfs(self.root); return res
    def find_intervals_containing(self, p):
        res = []
        def dfs(n):
            if not n: return
            if n.iv.overlaps_pt(p): res.append(n.iv)
            if n.left and n.left.maxEnd >= p: dfs(n.left)
            if n.right and p >= n.iv.start: dfs(n.right)
        dfs(self.root); return res
```

## When to Use

- Calendar and scheduling applications
- Resource booking and conflict detection
- Computational geometry problems
- Bioinformatics interval analysis
- Network bandwidth allocation

## Trade-offs

**Pros:**

- Efficient overlap queries O(log n + k)
- Supports range and point queries
- Dynamic insertion and deletion
- Better than naive O(n) overlap checking
- Useful for many real-world scheduling problems

**Cons:**

- More complex than simple data structures
- Requires balanced tree for good performance
- Memory overhead for storing max endpoints
- Not as cache-friendly as arrays

## Practice Problems

- **Meeting Rooms II**: Count minimum rooms needed
- **Merge Intervals**: Combine overlapping intervals
- **Insert Interval**: Add interval and merge if needed
- **Calendar Booking**: Implement booking system
- **Range Module**: Track and query ranges

<details>
<summary>Implementation Notes (Advanced)</summary>

### Tree Balancing

- **Red-Black Tree**: Self-balancing for guaranteed O(log n)
- **AVL Tree**: Stricter balancing for better search performance
- **Treap**: Randomized balancing with simpler implementation
- **Maintenance**: Update maxEnd during rotations

### Query Optimization

- **Pruning**: Skip subtrees that cannot contain overlaps
- **Range trees**: 2D extension for rectangle intersection
- **Segment trees**: Alternative for static interval sets
- **Fractional cascading**: Speed up multi-dimensional queries

### Memory Optimization

- **Compact representation**: Pack interval data efficiently
- **Node pooling**: Reuse deleted nodes
- **Lazy deletion**: Mark nodes as deleted instead of removing
- **Memory mapping**: For very large datasets

### Advanced Variants

- **Augmented trees**: Store additional aggregate information
- **Persistent interval trees**: Support historical queries
- **Parallel algorithms**: Concurrent interval tree operations
- **External memory**: Disk-based for large datasets

### Performance Considerations

- **Cache locality**: Consider memory layout
- **Batch operations**: Group insertions/deletions
- **Preprocessing**: Sort intervals for bulk loading
- **Approximate algorithms**: Trade accuracy for speed

</details>
