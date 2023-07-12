# Maximum Average Subarray 

## Problem Statement

You are given an integer array `nums` consisting of `n` elements, and an integer `k`.

The task is to find a contiguous subarray of length `k` in `nums` that has the maximum average value, and return this value. Any answer with a calculation error less than 10^-5 will be accepted.

## Example

**Input:**
nums = [1, 12, -5, -6, 50, 3], k = 4


**Output:**
12.75000


**Explanation:**

The maximum average is calculated as `(12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75`.

## Constraints

- n == nums.length
- 1 <= k <= n <= 10^5
- -10^4 <= nums[i] <= 10^4

## Solution Approach

The given solution is implemented in Python. Here's an explanation of the provided solution:

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        maxsum = sum(nums[0:k])
        s = maxsum
        for i in range(len(nums)-k):
            s = s - nums[i] + nums[i+k]
            maxsum = max(s, maxsum) 
        return round(maxsum/k, 5)
```

The solution defines a class with a method findMaxAverage that takes an integer array nums and an integer k as inputs and returns the maximum average value.

It initializes maxsum to the sum of the first k elements of nums. This is the initial maximum sum for the subarray.

It also initializes s to maxsum, which represents the current sum of the subarray.

The solution then iterates through the array nums from index 0 to len(nums)-k-1.

In each iteration, it updates s by subtracting nums[i] and adding nums[i+k]. This effectively moves the sliding window by one position to the right.

It updates maxsum with the maximum value between s and the current maxsum.

Finally, it calculates the maximum average by dividing maxsum by k and rounds the result to 5 decimal places before returning it.