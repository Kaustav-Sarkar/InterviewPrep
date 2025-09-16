import java.util.ArrayList;

/** Stdlib-backed wrapper scaffold for Array. */
public class ArrayStd {
    public static void main(String[] args) {
        ArrayList<Integer> numbers = new ArrayList<>();
        // Add elements using a loop
        for (int i = 1; i <= 5; i++) {
            numbers.add(i);
        }
        System.out.println("ArrayList after adding elements with loop: " + numbers);
        // Add a number at a specific index
        numbers.add(2, 99); // inserts 99 at index 2
        System.out.println("ArrayList after adding 99 at index 2: " + numbers);
        // Replace a number at a specific index
        numbers.set(4, 42); // replaces element at index 4 with 42
        System.out.println("ArrayList after replacing element at index 4 with 42: " + numbers);
        // Remove an element (e.g., remove element at index 3)
        numbers.remove(3);
        System.out.println("ArrayList after removing element at index 3: " + numbers);
    }
}
