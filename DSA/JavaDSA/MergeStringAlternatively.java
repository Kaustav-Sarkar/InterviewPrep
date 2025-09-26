
/*
meta:
  slug: merge-strings-alternately
  title: Merge Strings Alternately
  difficulty: easy
  tags: [string, two-pointers]
  platform: leetcode
  link: https://leetcode.com/problems/merge-strings-alternately/
  time: O(n+m)
  space: O(1)
question: Merge two strings by alternating characters starting from first.
approach: Iterate up to min length, then append remainder of longer string.
*/
class Solution {
    public String mergeAlternately(String word1, String word2) {
        int l1 = word1.length();
        int l2 = word2.length();
        int m;
        String n = "";
        String last = "";
        if (l1 > l2) {
            m = l2;
            last = word1.substring(m, l1);
        } else {
            m = l1;
            last = word2.substring(m, l2);
        }
        for (int i = 0; i < m; i++) {
            n = n + word1.charAt(i);
            n = n + word2.charAt(i);
        }
        n += last;
        return n;

    }
}