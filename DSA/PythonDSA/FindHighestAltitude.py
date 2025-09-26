"""
meta:
  slug: find-the-highest-altitude
  title: Find The Highest Altitude
  difficulty: easy
  tags: [array, prefix-sum]
  platform: leetcode
  link: https://leetcode.com/problems/find-the-highest-altitude/
  time: O(n)
  space: O(1)
question: Return the highest altitude given net gains between points.
approach: Accumulate gains tracking max prefix sum.
"""

class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        max_alt = 0
        curr_alt = 0
        for i in gain:
            curr_alt = curr_alt+i
            max_alt = max(curr_alt, max_alt)
        return max_alt