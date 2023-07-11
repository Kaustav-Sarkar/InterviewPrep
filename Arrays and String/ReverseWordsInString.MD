# Reverse Words in a String - Readme

## Problem Statement

Given an input string `s`, the task is to reverse the order of the words in the string.

A word is defined as a sequence of non-space characters. The words in `s` will be separated by at least one space.

Return a string of the words in reverse order concatenated by a single space.

Note that `s` may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.

## Example

**Input:**
s = "the sky is blue"

**Output:**
"blue is sky the"


**Explanation:**

The words in `s` are reversed: "the" becomes "the", "sky" becomes "is", "is" becomes "sky", and "blue" becomes "blue".

## Constraints

- 1 <= s.length <= 10^4
- `s` contains English letters (upper-case and lower-case), digits, and spaces ' '.
- There is at least one word in `s`.

## Solution Approach

The given solution is implemented in Python. Here's an explanation of the provided solution:

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split()         # Split the string into words
        words.reverse()           # Reverse the order of the words
        rev = ""
        for i in words:
            rev += i              # Concatenate each word to the result string
            rev += " "            # Add a single space after each word
        return rev[0:len(rev)-1]  # Remove the trailing space and return the result
```

The solution starts by splitting the input string s into words using the split() function. This will create a list of words.

The order of the words in the list is then reversed using the reverse() method.

A result string rev is initialized to store the reversed words.

The solution then iterates through each word in the reversed list of words. It concatenates each word to the result string rev and adds a single space after each word.

Finally, the trailing space is removed from the result string using string slicing ([0:len(rev)-1]) and the reversed string is returned.

The solution reverses the order of the words in the input string by splitting it into words, reversing the order of the words, and then concatenating them back into a string.