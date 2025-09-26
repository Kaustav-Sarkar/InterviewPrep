"""
meta:
  slug: maximum-average-subarray-i
  title: Maximum Average Subarray I
  difficulty: easy
  tags: [array, sliding-window]
  platform: leetcode
  link: https://leetcode.com/problems/maximum-average-subarray-i/
  time: O(n)
  space: O(1)
question: Find the contiguous subarray of length k with the maximum average.
approach: Sliding window maintaining sum of current window.
"""

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        maxsum = sum(nums[0:k])
        s = maxsum
        for i in range(len(nums)-k):
            s = s - nums[i] + nums[i+k]
            maxsum = max(s, maxsum) 
        return round(maxsum/k,5)