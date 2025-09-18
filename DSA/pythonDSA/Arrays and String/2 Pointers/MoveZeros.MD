# Move Zeroes to the End of Array - Readme

Given an integer array `nums`, the task is to move all zeros to the end of the array while maintaining the relative order of the non-zero elements. The solution should be implemented in-place, without creating a separate copy of the array.

## Example

**Input:**

nums = [0, 1, 0, 3, 12]

makefile
Copy code

**Output:**

[1, 3, 12, 0, 0]

yaml
Copy code

## Constraints

- 1 <= nums.length <= 10^4
- -2^31 <= nums[i] <= 2^31 - 1

## Solution Approach

The given solution is implemented in Python. Here's an explanation of the provided solution:

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        l = len(nums)    # Calculate the length of the array
        i = 0            # Initialize a pointer for iteration
        nonzero = 0      # Initialize a pointer to track the non-zero elements
        zero = 0         # Initialize a counter to track the number of zeros

        # Loop through the array
        while(i < l):
            if nums[i] == 0:
                zero += 1
            else:
                nums[nonzero] = nums[i]
                nonzero += 1
            i += 1

        # Replace the elements from index (l - zero) to l with zeros
        for i in range(l - zero, l):
            nums[i] = 0
```
The solution initializes a few variables to keep track of the number of zeros and the non-zero elements encountered.

It then iterates through the array using a while loop.

If the current element is zero, the zero counter is incremented.

If the current element is non-zero, it is placed at the position indicated by the nonzero pointer, and the nonzero pointer is incremented.

Finally, after iterating through the array, the remaining elements from index (l - zero) to l are replaced with zeros, effectively moving all zeros to the end of the array.

The solution modifies the input array in-place to achieve the desired result.