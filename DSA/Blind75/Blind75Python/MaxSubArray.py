"""
Given an integer array nums, find the

with the largest sum, and return its sum.

 

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

 

Constraints:

    1 <= nums.length <= 105
    -104 <= nums[i] <= 104

 

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""
class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        maxSum = nums[0]
        count = 0
        startIndex = 0
        finalStartIndex = 0
        endIndex = 0
        for i in range(len(nums)):
            count+=nums[i]
            if count>maxSum:
                maxSum = count
                endIndex = i
                finalStartIndex = startIndex

            if count < 0:
                count = 0
                startIndex = i+1
        print(nums[finalStartIndex: endIndex+1])
        return maxSum



