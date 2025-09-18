# Merge Strings Alternately - Readme

## Problem Statement

You are given two strings `word1` and `word2`. The task is to merge the strings by adding letters in alternating order, starting with `word1`. If one string is longer than the other, append the additional letters onto the end of the merged string. Return the merged string.

## Example

**Input:**
word1 = "abc", word2 = "pqr"

**Output:**
"apbqcr"


**Explanation:**

The merged string will be merged as follows:
word1: a b c
word2: p q r
merged: a p b q c r

## Constraints

- 1 <= word1.length, word2.length <= 100
- `word1` and `word2` consist of lowercase English letters.

## Solution Approach

The given solution is implemented in Java. Here's an explanation of the provided solution:

```java
class Solution {
    public String mergeAlternately(String word1, String word2) {
        int l1 = word1.length();
        int l2 = word2.length();
        int m;
        String n = "";
        String last = "";
        if (l1>l2){
            m = l2;
            last = word1.substring(m,l1);
        }else{
            m = l1;
            last = word2.substring(m,l2);
        }
        for (int i = 0; i<m;i++){
            n=n+word1.charAt(i);
            n=n+word2.charAt(i);
        }
        n+=last;
        return n;
        
    }
}
```
The solution first calculates the lengths of word1 and word2 using the length() method.

It initializes variables to store the merged string (n), the remaining portion of the longer string (last), and a counter (m) indicating the length of the shorter string.

Depending on which string is longer, the code assigns the length of the shorter string to m and stores the remaining portion of the longer string in last.

A for loop is used to iterate m times and add alternating characters from word1 and word2 to the merged string n.

Finally, the remaining portion of the longer string (last) is appended to n, and the merged string is returned.

The solution merges the strings by alternating characters and handles the case when one string is longer than the other by appending the additional letters onto the end of the merged string.
