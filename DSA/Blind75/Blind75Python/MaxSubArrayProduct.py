"""
Given an integer array nums, find a

that has the largest product, and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

 

Example 1:

Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

Example 2:

Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

 

Constraints:

    1 <= nums.length <= 2 * 104
    -10 <= nums[i] <= 10
    The product of any subarray of nums is guaranteed to fit in a 32-bit integer.
"""

class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        maxVal1 = max(nums)
        maxVal2 = maxVal1
        count1 = 1
        count2 = 1
        for i in nums:
            count1 *= i
            maxVal1 = max(count1, maxVal1)
            if count1 ==0:
                count1 = 1
        for i in nums[::-1]:
            count2 *= i
            maxVal2 = max(count2, maxVal2)
            if count2 ==0:
                count2 = 1
        return max(maxVal1, maxVal2)