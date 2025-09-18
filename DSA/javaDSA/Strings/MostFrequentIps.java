package DSA.javaDSA.Strings;

import java.util.Map;
import java.util.HashMap;
import java.util.Collections;

/*
You are given an array of strings, where each string represents a server log entry. Each log entry is formatted as "IP_ADDRESS - OTHER_INFO".
Write a method public String findMostFrequentIp(String[] logs) that processes these logs and returns the IP address that appears most frequently. 
If there's a tie, you can return any of the most frequent IPs.

Example:
String[] logs = {
  "10.0.0.1 - GET /home",
  "10.0.0.2 - GET /about",
  "10.0.0.1 - POST /login",
  "10.0.0.3 - GET /home",
  "10.0.0.1 - GET /logout",
  "10.0.0.2 - GET /home"
};
 */
public class MostFrequentIps {

    public static String mostFrequentIps(String[] logs) {
        Map<String, Integer> ipCounter = new HashMap<>();
        for (String log : logs) {
            String ip = log.split("-")[0];
            ip = ip.strip();
            if (!ipCounter.containsKey(ip)) {
                ipCounter.put(ip, 1);
            } else {
                int val = ipCounter.get(ip);
                ipCounter.put(ip, val + 1);
            }
        }
        // for (Map.Entry<String, Integer> value: ipCounter.entrySet()){ // the easiest
        // way to traverse a hashmap
        // value.getKey();
        // value.getValue();
        // }
        int maxValue = Collections.max(ipCounter.values());
        return ipCounter.entrySet().stream().filter(entry -> entry.getValue() == maxValue).findFirst()
                .map(Map.Entry::getKey).orElse("");

        /*
         * For interviews stick to this, it can loop over any Map
         * 
         * for (Map.Entry<String, String> entry : capitalCities.entrySet()) {
         * String key = entry.getKey();
         * String value = entry.getValue();
         * System.out.println("Key: " + key + ", Value: " + value);
         * }
         * 
         * 
         * COMPREHENSIVE EXPLANATION OF STREAM API AND MAP SYNTAX:
         * 
         * === MAP.ENTRY EXPLAINED ===
         * Map.Entry<String, Integer> represents a key-value pair from HashMap
         * - entry.getKey() returns the IP address (String)
         * - entry.getValue() returns the frequency count (Integer)
         * - ipCounter.entrySet() converts HashMap to Set<Map.Entry<String, Integer>>
         * 
         * === LAMBDA EXPRESSIONS EXPLAINED ===
         * Lambda syntax: (parameters) -> expression
         * - entry -> entry.getValue() == maxValue
         * This is a function that takes an entry and returns true/false
         * Traditional equivalent: new Predicate<Map.Entry<String, Integer>>() {
         * public boolean test(Map.Entry<String, Integer> entry) {
         * return entry.getValue() == maxValue;
         * }
         * }
         * 
         * === METHOD REFERENCES EXPLAINED ===
         * Map.Entry::getKey is shorthand for entry -> entry.getKey()
         * - :: is the method reference operator
         * - ClassName::methodName refers to a method
         * - More readable than lambda when just calling one method
         * 
         * === STREAM API CHAIN EXPLAINED ===
         * .stream() - Converts collection to Stream for functional operations
         * .filter() - Keeps only elements that match the condition (predicate)
         * .max() - Finds maximum element using provided comparator
         * .findFirst() - Returns first element wrapped in Optional
         * .map() - Transforms each element (entry -> key)
         * .orElse() - Provides default value if Optional is empty
         * 
         * === OPTIONAL EXPLAINED ===
         * Optional<T> is a wrapper that may or may not contain a value
         * - Prevents NullPointerException
         * - .orElse("") returns "" if Optional is empty
         * - Modern Java's way of handling potential null values
         * 
         * === COMPARATOR EXPLAINED ===
         * Map.Entry.comparingByValue() creates a Comparator that compares entries by
         * their values
         * - Used with .max() to find entry with highest value
         * - No need to manually find maxValue first
         * 
         * OPTION 1 - Most Efficient (Direct max without pre-calculation):
         * 
         * return ipCounter.entrySet().stream()
         * .max(Map.Entry.comparingByValue())
         * .map(Map.Entry::getKey)
         * .orElse("");
         * 
         * 
         * OPTION 2 - Traditional loop (Most readable for beginners):
         * String mostFrequentIp = "";
         * int maxCount = 0;
         * 
         * for (Map.Entry<String, Integer> entry : ipCounter.entrySet()) {
         * if (entry.getValue() > maxCount) {
         * maxCount = entry.getValue();
         * mostFrequentIp = entry.getKey();
         * }
         * }
         * return mostFrequentIp;
         * 
         * OPTION 3 - Filter with pre-calculated max (Your original approach):
         * int maxValue = Collections.max(ipCounter.values());
         * return ipCounter.entrySet().stream()
         * .filter(entry -> entry.getValue() == maxValue)
         * .findFirst()
         * .map(Map.Entry::getKey)
         * .orElse("");
         * 
         * WHY OPTION 1 IS MOST EFFICIENT:
         * - Only one pass through the data (O(n))
         * - No need to calculate maxValue separately
         * - Cleaner, more functional programming style
         * - Built-in null safety with Optional
         */

    }

    public static void main(String[] args) {
        String[] logs = {
                "10.0.0.1 - GET /home",
                "10.0.0.2 - GET /about",
                "10.0.0.1 - POST /login",
                "10.0.0.3 - GET /home",
                "10.0.0.1 - GET /logout",
                "10.0.0.2 - GET /home"
        };
        System.out.println(mostFrequentIps(logs));
    }
}
