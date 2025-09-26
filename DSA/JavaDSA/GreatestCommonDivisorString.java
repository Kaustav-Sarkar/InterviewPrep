
/*
meta:
  slug: greatest-common-divisor-of-strings
  title: Greatest Common Divisor of Strings
  difficulty: easy
  tags: [string, math]
  platform: leetcode
  link: https://leetcode.com/problems/greatest-common-divisor-of-strings/
  time: O(n+m)
  space: O(1)
question: Find the largest string that divides both input strings.
approach: Recursive reduction by suffix match; akin to Euclidean algorithm.
*/
class Solution {
    private String gcd(String str1, String str2) {
        if (str1.equals(str2)) {
            return str1;
        }
        int l2 = str2.length();
        int l1 = str1.length();
        String temp;
        int n;
        if (str2.equals("")) {
            return str1;
        }
        if (str1.equals("")) {
            return str2;
        }
        if (l2 > l1) {
            n = l2;
            l2 = l1;
            l1 = n;
            temp = str2;
            str2 = str1;
            str1 = temp;
        }
        if (str2.equals(str1.substring(l1 - l2, l1))) {
            return gcd(str2, str1.substring(0, l1 - l2));
        }
        return "";

    }

    public String gcdOfStrings(String str1, String str2) {
        if (str1.equals(str2)) {
            return str1;
        }
        return gcd(str1, str2);

    }
}