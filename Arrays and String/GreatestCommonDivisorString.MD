# Greatest Common Divisor of Strings - Readme

## Problem Statement

For two strings `s` and `t`, we say "t divides s" if and only if s = t + ... + t (i.e., t is concatenated with itself one or more times).

Given two strings `str1` and `str2`, the task is to return the largest string `x` such that `x` divides both `str1` and `str2`.

## Example

**Input:**
str1 = "ABCABC", str2 = "ABC"
**Output:**
"ABC"


**Explanation:**

Both `str1` and `str2` are divisible by "ABC".

## Constraints

- 1 <= str1.length, str2.length <= 1000
- `str1` and `str2` consist of English uppercase letters.

## Solution Approach

The given solution is implemented in Java. Here's an explanation of the provided solution:

```java
class Solution {
    private String gcd(String str1, String str2){
        if (str1.equals(str2)){
            return str1;
        }
        int l2 = str2.length();
        int l1 = str1.length();
        String temp;
        int n;
        if (str2.equals("")){
            return str1;
        }
        if (str1.equals("")){
            return str2;
        }
        if (l2>l1){
            n = l2;
            l2 = l1;
            l1 = n;
            temp = str2;
            str2 = str1;
            str1 = temp;
        }
        if (str2.equals(str1.substring(l1-l2,l1))){
            return gcd(str2, str1.substring(0,l1-l2));
        }
        return "";
        
    }
    public String gcdOfStrings(String str1, String str2) {
        if (str1.equals(str2)){
            return str1;
        }
        return gcd(str1,str2);

    }
}
```

The solution defines a private recursive method gcd (greatest common divisor) that takes two strings as parameters and returns the largest string that divides both of them.

The gcd method checks if the two input strings are equal. If they are equal, it returns one of the strings as the result.

The method then compares the lengths of the two strings and swaps them if necessary, ensuring that str1 is always longer than or equal to str2.

If one of the strings is empty, it means the other string is the divisor, so the non-empty string is returned as the result.

The method then checks if str2 is a substring of the end portion of str1. If it is, it recursively calls the gcd method with str2 and the remaining portion of str1.

If none of the above conditions are satisfied, it means the strings do not have a common divisor, so an empty string is returned.

The public method gcdOfStrings checks if the two input strings are equal. If they are, it returns one of the strings as the result. Otherwise, it calls the gcd method to find the greatest common divisor of the strings.