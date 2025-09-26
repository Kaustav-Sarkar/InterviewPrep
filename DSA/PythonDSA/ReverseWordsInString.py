"""
meta:
  slug: reverse-words-in-a-string
  title: Reverse Words in a String
  difficulty: medium
  tags: [string, two-pointers]
  platform: leetcode
  link: https://leetcode.com/problems/reverse-words-in-a-string/
  time: O(n)
  space: O(n)
question: Reverse the order of words; no leading/trailing or multiple spaces.
approach: Split, reverse list, join with single spaces.
"""

class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()
        words.reverse()
        rev = ""
        for i in words:
            rev+=i
            rev+=" "
        return rev[0:len(rev)-1]