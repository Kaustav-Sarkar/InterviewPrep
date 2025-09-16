# Ordered Set (TreeSet)

## Quick Definition

Set that maintains elements in sorted order using a balanced binary search tree. Provides O(log n) operations with automatic ordering.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add | **O(log n)** | O(n) |
| Remove | **O(log n)** | — |
| Contains | **O(log n)** | — |
| Range Operations | O(log n + k) | — |

## Core Operations

```java
// Basic TreeSet operations
TreeSet<Integer> set = new TreeSet<>();

// Insertion maintains sorted order
set.add(30); set.add(10); set.add(50); set.add(20);
System.out.println(set);  // [10, 20, 30, 50]

// Basic operations
boolean exists = set.contains(20);    // true
boolean removed = set.remove(30);     // true
int size = set.size();                // 3

// Range operations
TreeSet<Integer> nums = new TreeSet<>();
for (int i : Arrays.asList(1, 3, 5, 7, 9, 11, 13)) {
    nums.add(i);
}

// Navigation methods
Integer first = nums.first();         // 1
Integer last = nums.last();           // 13
Integer lower = nums.lower(7);        // 5 (largest < 7)
Integer floor = nums.floor(6);        // 5 (largest ≤ 6)
Integer ceiling = nums.ceiling(6);    // 7 (smallest ≥ 6)
Integer higher = nums.higher(7);      // 9 (smallest > 7)

// Range views
NavigableSet<Integer> subSet = nums.subSet(3, true, 9, false);  // [3, 9)
NavigableSet<Integer> headSet = nums.headSet(7, false);         // < 7
NavigableSet<Integer> tailSet = nums.tailSet(7, true);          // ≥ 7

// Poll operations (remove and return)
Integer pollFirst = nums.pollFirst();  // removes and returns 1
Integer pollLast = nums.pollLast();    // removes and returns 13

// Set operations
TreeSet<Integer> set1 = new TreeSet<>(Arrays.asList(1, 2, 3, 4));
TreeSet<Integer> set2 = new TreeSet<>(Arrays.asList(3, 4, 5, 6));

// Union
TreeSet<Integer> union = new TreeSet<>(set1);
union.addAll(set2);  // [1, 2, 3, 4, 5, 6]

// Intersection
TreeSet<Integer> intersection = new TreeSet<>(set1);
intersection.retainAll(set2);  // [3, 4]

// Difference
TreeSet<Integer> difference = new TreeSet<>(set1);
difference.removeAll(set2);  // [1, 2]

// Custom comparator
TreeSet<String> reverseSet = new TreeSet<>(Collections.reverseOrder());
reverseSet.addAll(Arrays.asList("zebra", "apple", "banana"));
System.out.println(reverseSet);  // [zebra, banana, apple]

// Meeting rooms scheduler
class MeetingScheduler {
    private TreeSet<int[]> meetings = new TreeSet<>((a, b) -> 
        a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    
    public boolean book(int start, int end) {
        int[] newMeeting = {start, end};
        
        // Check overlap with previous meeting
        int[] prev = meetings.floor(newMeeting);
        if (prev != null && prev[1] > start) {
            return false;
        }
        
        // Check overlap with next meeting
        int[] next = meetings.ceiling(newMeeting);
        if (next != null && next[0] < end) {
            return false;
        }
        
        meetings.add(newMeeting);
        return true;
    }
}
```

## Python Snippet

```python
# Ordered set via sorted list (for small N) or 'sortedcontainers.SortedSet'
import bisect

class OrderedSet:
    def __init__(self): self.a = []
    def add(self, x):
        i = bisect.bisect_left(self.a, x)
        if i == len(self.a) or self.a[i] != x: self.a.insert(i, x)
    def remove(self, x):
        i = bisect.bisect_left(self.a, x)
        if i < len(self.a) and self.a[i] == x: self.a.pop(i)
    def contains(self, x):
        i = bisect.bisect_left(self.a, x); return i < len(self.a) and self.a[i] == x
    def first(self): return self.a[0]
    def last(self): return self.a[-1]
    def lower(self, x):
        i = bisect.bisect_left(self.a, x); return self.a[i-1] if i > 0 else None
    def floor(self, x):
        i = bisect.bisect_right(self.a, x); return self.a[i-1] if i > 0 else None
    def ceiling(self, x):
        i = bisect.bisect_left(self.a, x); return self.a[i] if i < len(self.a) else None
    def higher(self, x):
        i = bisect.bisect_right(self.a, x); return self.a[i] if i < len(self.a) else None
    def subset(self, lo, hi, lo_inc=True, hi_inc=False):
        i = bisect.bisect_left(self.a, lo) if lo_inc else bisect.bisect_right(self.a, lo)
        j = bisect.bisect_right(self.a, hi) if hi_inc else bisect.bisect_left(self.a, hi)
        return self.a[i:j]
```

## When to Use

- Maintaining sorted unique elements
- Range queries on ordered data
- Finding closest elements (floor, ceiling)
- Sliding window problems requiring order
- Duplicate elimination with ordering

## Trade-offs

**Pros:**

- Elements always in sorted order
- Automatic duplicate elimination
- Efficient range operations
- O(log n) guaranteed performance
- Rich navigation API

**Cons:**

- Slower than HashSet for basic operations
- Higher memory overhead
- Elements must be comparable
- No O(1) operations

## Practice Problems

- **Contains Duplicate III**: Use TreeSet for range checking
- **Sliding Window Maximum**: TreeSet for maintaining window elements
- **Meeting Rooms**: TreeSet for interval overlap detection
- **Kth Smallest Element in Sorted Matrix**: TreeSet for candidates
- **Range Sum Query**: TreeSet with coordinate compression

<details>
<summary>Implementation Notes (Advanced)</summary>

### TreeSet Internals

- **Red-Black Tree**: Java's TreeSet uses Red-Black tree implementation
- **Comparison**: Uses Comparable or Comparator for ordering
- **Null elements**: Not allowed (would break comparison)
- **Thread safety**: Not thread-safe, use ConcurrentSkipListSet for concurrency

### Performance Characteristics

- **Guaranteed O(log n)**: Unlike HashSet's amortized O(1)
- **Memory overhead**: Each node has color bit + 2 pointers + parent reference
- **Cache locality**: Poor compared to arrays, better than general trees

### Navigation Operations

- **Range views**: SubSet, headSet, tailSet are live views
- **Polling operations**: pollFirst(), pollLast() remove and return
- **Null handling**: Methods return null for non-existent elements

</details>
