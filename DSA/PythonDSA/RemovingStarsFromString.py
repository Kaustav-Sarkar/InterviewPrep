"""
meta:
  slug: removing-stars-from-a-string
  title: Removing Stars From a String
  difficulty: medium
  tags: [stack, string]
  platform: leetcode
  link: https://leetcode.com/problems/removing-stars-from-a-string/
  time: O(n)
  space: O(n)
question: Process '*' as backspace; return final string.
approach: Use list as stack; push letters, pop on '*'.
"""

class Solution:
    def removeStars(self, s: str) -> str:
        l = []
        for i in range(len(s)):
            if s[i]!="*":
                l.append(s[i])
            else:
                l.pop()
        
        return "".join(l)