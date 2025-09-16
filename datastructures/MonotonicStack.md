# Monotonic Stack

## Quick Definition

Stack that maintains elements in monotonic (increasing or decreasing) order. Elements that violate the ordering are popped before insertion. Powerful for range queries.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Push | **O(1)** amortized | O(n) |
| Pop | **O(1)** | — |
| Peek | **O(1)** | — |
| Process Array | O(n) | — |

## Core Operations

```java
// Monotonic increasing stack (bottom to top)
class MonotonicIncreasingStack {
    private ArrayDeque<Integer> stack = new ArrayDeque<>();
    
    public void push(int val) {
        // Remove all elements greater than current value
        while (!stack.isEmpty() && stack.peek() > val) {
            stack.pop();
        }
        stack.push(val);
    }
    
    public Integer peek() { return stack.peek(); }
    public Integer pop() { return stack.pop(); }
    public boolean isEmpty() { return stack.isEmpty(); }
}

// Next Greater Element pattern
int[] nextGreaterElement(int[] nums) {
    int n = nums.length;
    int[] result = new int[n];
    ArrayDeque<Integer> stack = new ArrayDeque<>();  // stores indices
    
    // Process from right to left
    for (int i = n - 1; i >= 0; i--) {
        // Pop smaller elements
        while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
            stack.pop();
        }
        
        result[i] = stack.isEmpty() ? -1 : nums[stack.peek()];
        stack.push(i);
    }
    return result;
}

// Largest Rectangle in Histogram
int largestRectangle(int[] heights) {
    ArrayDeque<Integer> stack = new ArrayDeque<>();  // indices of increasing heights
    int maxArea = 0;
    
    for (int i = 0; i <= heights.length; i++) {
        int h = (i == heights.length) ? 0 : heights[i];
        
        // Pop heights greater than current
        while (!stack.isEmpty() && heights[stack.peek()] > h) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
}

// Daily Temperatures (next warmer day)
int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] result = new int[n];
    ArrayDeque<Integer> stack = new ArrayDeque<>();  // indices
    
    for (int i = 0; i < n; i++) {
        // Pop days with lower temperature
        while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
            int prevDay = stack.pop();
            result[prevDay] = i - prevDay;
        }
        stack.push(i);
    }
    return result;
}

// Remove K Digits to make smallest number
String removeKdigits(String num, int k) {
    ArrayDeque<Character> stack = new ArrayDeque<>();
    int toRemove = k;
    
    for (char digit : num.toCharArray()) {
        // Remove larger digits from end
        while (!stack.isEmpty() && toRemove > 0 && stack.peek() > digit) {
            stack.pop();
            toRemove--;
        }
        stack.push(digit);
    }
    
    // Remove remaining digits from end
    while (toRemove > 0) {
        stack.pop();
        toRemove--;
    }
    
    // Build result
    StringBuilder result = new StringBuilder();
    while (!stack.isEmpty()) {
        result.append(stack.removeLast());  // reverse order
    }
    
    // Remove leading zeros
    while (result.length() > 0 && result.charAt(0) == '0') {
        result.deleteCharAt(0);
    }
    
    return result.length() == 0 ? "0" : result.toString();
}

// Trapping Rain Water
int trapRainWater(int[] height) {
    ArrayDeque<Integer> stack = new ArrayDeque<>();  // indices
    int water = 0;
    
    for (int i = 0; i < height.length; i++) {
        while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
            int bottom = stack.pop();
            if (stack.isEmpty()) break;
            
            int distance = i - stack.peek() - 1;
            int boundedHeight = Math.min(height[i], height[stack.peek()]) - height[bottom];
            water += distance * boundedHeight;
        }
        stack.push(i);
    }
    return water;
}

// Sum of Subarray Minimums
int sumSubarrayMins(int[] arr) {
    int MOD = 1_000_000_007;
    int n = arr.length;
    
    // Find previous and next smaller elements
    int[] prevSmaller = new int[n];
    int[] nextSmaller = new int[n];
    
    ArrayDeque<Integer> stack = new ArrayDeque<>();
    
    // Previous smaller elements
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && arr[stack.peek()] >= arr[i]) {
            stack.pop();
        }
        prevSmaller[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }
    
    stack.clear();
    
    // Next smaller elements
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.isEmpty() && arr[stack.peek()] > arr[i]) {
            stack.pop();
        }
        nextSmaller[i] = stack.isEmpty() ? n : stack.peek();
        stack.push(i);
    }
    
    long result = 0;
    for (int i = 0; i < n; i++) {
        long left = i - prevSmaller[i];
        long right = nextSmaller[i] - i;
        result = (result + (arr[i] * left * right) % MOD) % MOD;
    }
    
    return (int) result;
}
```

## Python Snippet

```python
from collections import deque

def next_greater(nums):
    n = len(nums); res = [-1]*n; st = []
    for i in range(n-1, -1, -1):
        while st and nums[st[-1]] <= nums[i]: st.pop()
        res[i] = -1 if not st else nums[st[-1]]
        st.append(i)
    return res

def largest_rectangle(heights):
    st = []; ans = 0
    for i in range(len(heights)+1):
        h = 0 if i == len(heights) else heights[i]
        while st and heights[st[-1]] > h:
            height = heights[st.pop()]
            width = i if not st else i - st[-1] - 1
            ans = max(ans, height*width)
        st.append(i)
    return ans

def daily_temperatures(T):
    n = len(T); res = [0]*n; st = []
    for i, t in enumerate(T):
        while st and T[st[-1]] < t:
            j = st.pop(); res[j] = i - j
        st.append(i)
    return res
```

## When to Use

- Finding next/previous greater/smaller elements
- Histogram and rectangle area problems
- Range minimum/maximum queries in arrays
- Eliminating elements that will never be optimal
- Stock span and financial analysis problems

## Trade-offs

**Pros:**

- O(n) total time for processing arrays
- Elegant solution for range optimization problems
- Memory-efficient for sparse optimal solutions
- Natural fit for many geometric problems

**Cons:**

- Limited to specific problem patterns
- Can be non-intuitive for beginners
- Destroys original element order
- May require careful handling of edge cases

## Practice Problems

- **Next Greater Element**: Use monotonic decreasing stack
- **Largest Rectangle in Histogram**: Classic monotonic stack problem
- **Daily Temperatures**: Find next warmer day
- **Remove K Digits**: Make smallest number using monotonic stack
- **Trapping Rain Water**: Calculate trapped water using stack

<details>
<summary>Implementation Notes (Advanced)</summary>

### Stack Variants

- **Monotonic increasing**: Each element ≥ previous element
- **Monotonic decreasing**: Each element ≤ previous element
- **Strictly monotonic**: No equal elements allowed
- **Non-strictly monotonic**: Equal elements allowed

### Common Patterns

- **Store indices**: Often more useful than storing values directly
- **Process from right**: For "next greater" type problems
- **Process from left**: For "previous smaller" type problems
- **Sentinel values**: Add boundary elements to simplify logic

### Optimization Techniques

- **Early termination**: Stop when stack becomes empty
- **Batch processing**: Handle multiple queries together
- **Space optimization**: Use arrays instead of explicit stack when possible
- **Boundary handling**: Add virtual elements to avoid special cases

### Problem Recognition

- **Range optimization**: When each element affects a range of positions
- **Visibility problems**: When elements "block" others
- **Contribution counting**: When elements contribute to multiple subarrays
- **Greedy elimination**: When some elements are clearly suboptimal

</details>
