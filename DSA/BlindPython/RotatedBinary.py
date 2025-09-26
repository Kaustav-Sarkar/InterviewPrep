"""
There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

 

Example 1:

Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:

Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:

Input: nums = [1], target = 0
Output: -1

 

Constraints:

    1 <= nums.length <= 5000
    -104 <= nums[i] <= 104
    All values of nums are unique.
    nums is an ascending array that is possibly rotated.
    -104 <= target <= 104

 

"""


class Solution:
    def binary(self,l,r,nums, target):
        if (l>r):
            return -1
        mid = (l+r)//2
        if target < nums[mid]:
            return self.binary(l, mid-1, nums, target)
        elif target > nums[mid]:
            return self.binary(mid+1, r, nums, target)
        else:
            return mid
    def rotatedBinary(self, left, right, nums, target):
        if left>right:
            return -1
        mid = (left+right)//2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if (nums[left]<=target<nums[mid]):
                return self.rotatedBinary(left, mid-1, nums, target)w
            else:
                return self.rotatedBinary(mid+1, right, nums, target)
        else:
            if (nums[mid]<target<=nums[right]):
                return self.rotatedBinary(mid+1, right, nums, target)
            else:
                return self.rotatedBinary(left, mid-1, nums, target)

    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)-1
        return self.rotatedBinary(left, right, nums, target)
        
            
