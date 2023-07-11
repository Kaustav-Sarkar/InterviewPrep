class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()
        words.reverse()
        rev = ""
        for i in words:
            rev+=i
            rev+=" "
        return rev[0:len(rev)-1]