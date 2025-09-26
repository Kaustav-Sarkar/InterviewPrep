/*
meta:
  slug: valid-palindrome
  title: Valid Palindrome (Simple)
  difficulty: easy
  tags: [two-pointers, string]
  platform: custom
  link: null
  time: O(n)
  space: O(1)
question: Check whether a string is palindrome.
approach: Compare symmetric characters from ends moving inward.
*/

public class Palindrome {

    public static boolean isPalindrome(String s) {
        for (int i = 0; i < (s.length() / 2); i++) {
            // System.out.println(s.charAt(i) + s.charAt(s.length() - i - 1));
            if (s.charAt(i) != s.charAt(s.length() - i - 1)) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("racecar"));
        System.out.println(isPalindrome("hello"));
        System.out.println(isPalindrome("helloolleh"));
        System.out.println(isPalindrome("helloooolleh"));
        System.out.println(isPalindrome("hellooooolleh"));

    }
}
