"""
Given a string s, return the longest

in s.

 

Example 1:

Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:

Input: s = "cbbd"
Output: "bb"

 

Constraints:

    1 <= s.length <= 1000
    s consist of only digits and English letters.

 
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        firstIndex = 0
        lastIndex = 0
        longestLength = 0
        strLen = len(s)
        # 2 cases needed if the palindrone is odd and if its even eg bb will never work with odd palindrome while loop
        for i in range(strLen):
            # odd loop
            l,r = i,i
            while (l>=0 and r<strLen) and s[l] == s[r]:
                if r-l+1 > longestLength:
                    firstIndex = l
                    lastIndex = r
                    longestLength = r-l+1
                l-=1
                r+=1
            
            l,r = i,i+1
            while (l>=0 and r<strLen) and s[l] == s[r]:
                if r-l+1 > longestLength:
                    firstIndex = l
                    lastIndex = r
                    longestLength = r-l+1
                l-=1
                r+=1
        return s[firstIndex:lastIndex+1]
            
