# Monotonic Queue

## Quick Definition

Deque that maintains elements in monotonic order while supporting efficient insertion/deletion at both ends. Optimized for sliding window maximum/minimum problems.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Push Back | **O(1)** amortized | O(k) |
| Pop Front | **O(1)** | — |
| Get Max/Min | **O(1)** | — |
| Process Array | O(n) | — |

## Core Operations

```java
// Sliding Window Maximum (classic problem)
int[] slidingWindowMaximum(int[] nums, int k) {
    if (nums.length == 0 || k == 0) return new int[0];
    
    int n = nums.length;
    int[] result = new int[n - k + 1];
    ArrayDeque<Integer> deque = new ArrayDeque<>();  // stores indices
    
    for (int i = 0; i < n; i++) {
        // Remove indices outside current window
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }
        
        // Remove smaller elements from back (maintain decreasing order)
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[i]) {
            deque.pollLast();
        }
        
        deque.offerLast(i);
        
        // Add to result when window is fully formed
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }
    return result;
}

// Sliding Window Minimum
int[] slidingWindowMinimum(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    ArrayDeque<Integer> deque = new ArrayDeque<>();  // increasing order for minimum
    
    for (int i = 0; i < n; i++) {
        // Remove indices outside window
        while (!deque.isEmpty() && deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }
        
        // Remove larger elements from back (maintain increasing order)
        while (!deque.isEmpty() && nums[deque.peekLast()] >= nums[i]) {
            deque.pollLast();
        }
        
        deque.offerLast(i);
        
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }
    return result;
}

// Constrained Subsequence Sum
int constrainedSubsetSum(int[] nums, int k) {
    int n = nums.length;
    int[] dp = new int[n];
    ArrayDeque<Integer> deque = new ArrayDeque<>();  // indices of dp values
    
    for (int i = 0; i < n; i++) {
        // Remove indices outside window
        while (!deque.isEmpty() && deque.peekFirst() < i - k) {
            deque.pollFirst();
        }
        
        // dp[i] = nums[i] + max(0, max_in_window)
        dp[i] = nums[i] + (deque.isEmpty() ? 0 : Math.max(0, dp[deque.peekFirst()]));
        
        // Maintain decreasing order in deque
        while (!deque.isEmpty() && dp[deque.peekLast()] <= dp[i]) {
            deque.pollLast();
        }
        
        deque.offerLast(i);
    }
    
    return Arrays.stream(dp).max().getAsInt();
}

// Generic template for different ordering
class MonotonicDeque {
    private ArrayDeque<Integer> deque = new ArrayDeque<>();
    
    // For maximum queries (decreasing order)
    public void pushForMax(int[] arr, int i) {
        while (!deque.isEmpty() && arr[deque.peekLast()] <= arr[i]) {
            deque.pollLast();
        }
        deque.offerLast(i);
    }
    
    // For minimum queries (increasing order)
    public void pushForMin(int[] arr, int i) {
        while (!deque.isEmpty() && arr[deque.peekLast()] >= arr[i]) {
            deque.pollLast();
        }
        deque.offerLast(i);
    }
    
    public void popOutside(int left) {
        while (!deque.isEmpty() && deque.peekFirst() < left) {
            deque.pollFirst();
        }
    }
    
    public Integer getExtreme() {
        return deque.isEmpty() ? null : deque.peekFirst();
    }
}
```

## Python Snippet

```python
from collections import deque

def sliding_window_max(nums, k):
    if not nums or k == 0: return []
    dq, res = deque(), []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k: dq.popleft()
        while dq and nums[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if i >= k - 1: res.append(nums[dq[0]])
    return res

def sliding_window_min(nums, k):
    if not nums or k == 0: return []
    dq, res = deque(), []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k: dq.popleft()
        while dq and nums[dq[-1]] >= x: dq.pop()
        dq.append(i)
        if i >= k - 1: res.append(nums[dq[0]])
    return res
```

## When to Use

- Sliding window maximum/minimum problems
- Range queries on subarrays with size constraints
- Dynamic programming with range optimization
- Online algorithms processing streaming data
- Maintaining extremes in moving windows

## Trade-offs

**Pros:**

- O(1) amortized insertion and deletion
- O(1) access to window maximum/minimum
- Efficient for sliding window problems
- Works well with streaming data

**Cons:**

- Limited to specific problem patterns
- Requires careful implementation
- May not be intuitive for beginners
- Not suitable for random access patterns

## Practice Problems

- **Sliding Window Maximum**: Classic monotonic queue application
- **Shortest Subarray with Sum at Least K**: Use with prefix sums
- **Constrained Subsequence Sum**: Dynamic programming with window constraint
- **Jump Game VI**: Maximum score with jump constraints
- **Longest Continuous Subarray**: Monotonic queue for range constraints

<details>
<summary>Implementation Notes (Advanced)</summary>

### Queue Variants

- **Monotonic increasing**: For minimum queries (smaller elements at front)
- **Monotonic decreasing**: For maximum queries (larger elements at front)
- **Non-strict**: Allow equal elements
- **Strict**: Remove equal elements

### Window Management

- **Index tracking**: Store indices instead of values for position awareness
- **Boundary conditions**: Handle window formation and expiration
- **Multiple windows**: Process overlapping or adjacent windows

### Problem Recognition

- **Fixed window size**: Classic sliding window maximum/minimum
- **Variable constraints**: Shortest/longest subarray problems
- **DP optimization**: Range maximum queries in recurrence relations

</details>
