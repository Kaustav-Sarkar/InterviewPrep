package DSA.javaDSA.Strings;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;

public class Anagram {
    public static List<List<String>> groupAnagrams(String[] strs) {
        List<List<String>> s = new ArrayList<>();
        Map<String, List<String>> anagrams = new HashMap<>();
        for (String str1 : strs) {
            char[] str2 = str1.toCharArray();
            Arrays.sort(str2);
            String str3 = String.valueOf(str2);
            var listOfWords = anagrams.getOrDefault(str3, new ArrayList<>());
            listOfWords.add(str1);
            anagrams.put(str3, listOfWords);
        }
        for (Map.Entry<String, List<String>> finalAnswer : anagrams.entrySet()) {
            s.add(finalAnswer.getValue()); // one way of getting all values
        }
        return new ArrayList<>(anagrams.values());
    }

    /*
     * Sorting in Java
     * For Strings (sort characters):
     * ;
     * 
     * String sorted = str.chars().sorted()
     * .collect(StringBuilder::new, StringBuilder::appendCodePoint,
     * StringBuilder::append)
     * .toString();
     * 
     * Simple alternative for Strings:
     * ;
     * 
     * char[] chars = str.toCharArray();
     * Arrays.sort(chars);
     * String sorted = new String(chars);
     * 
     * 
     * For Lists:
     * list
     * 
     * 
     * Collections.sort(list); // In-place sorting
     * // or
     * list.sort(null); // In-place sorting (Java 8+)
     * // or
     * List<String> sorted = list.stream().sorted().collect(Collectors.toList()); //
     * New list
     * 
     * 
     * Reason: Arrays.sort() is most efficient for strings converted to char arrays.
     * Collections.sort() or List.sort() are standard for lists. The char array
     * approach is simpler and more readable than the stream approach for strings.
     */

    public static void main(String[] args) {
        String[] strs = { "eat", "tea", "tan", "ate", "nat", "bat" };
        System.out.println(groupAnagrams(strs));
    }

}
