# Remove Stars - Readme

## Problem Statement

You are given a string `s`, which contains stars `*`.

In one operation, you can:
- Choose a star in `s`.
- Remove the closest non-star character to its left, as well as remove the star itself.

Return the string after all stars have been removed.

**Note:**

- The input will be generated such that the operation is always possible.
- It can be shown that the resulting string will always be unique.

## Example

**Input:**
```s = "leet**cod*e"```

**Output:**
```"lecoe"```

**Explanation:**

Performing the removals from left to right:
- The closest character to the 1st star is 't' in "leet**cod*e". `s` becomes "lee*cod*e".
- The closest character to the 2nd star is 'e' in "lee*cod*e". `s` becomes "lecod*e".
- The closest character to the 3rd star is 'd' in "lecod*e". `s` becomes "lecoe".
There are no more stars, so we return "lecoe".

## Constraints

- 1 <= s.length <= 10^5
- `s` consists of lowercase English letters and stars `*`.
- The operation above can be performed on `s`.

## Solution Approach

The given solution is implemented in Python. Here's an explanation of the provided solution:

```python
class Solution:
    def removeStars(self, s: str) -> str:
        l = []
        for i in range(len(s)):
            if s[i] != "*":
                l.append(s[i])
            else:
                l.pop()
        return "".join(l)
```
The solution defines a class with a method removeStars that takes a string s as input and returns the modified string after removing stars.

The solution uses a list l to simulate the removal process. It iterates through the characters of the input string s.

If the current character is not a star, it appends the character to the list l.

If the current character is a star, it removes the last non-star character from the list l using the pop() function.

Finally, it joins the characters in the list l together to form a string and returns the result.

The solution performs the removal operation by iterating through the string and simulating the removal of stars and their closest non-star characters.






