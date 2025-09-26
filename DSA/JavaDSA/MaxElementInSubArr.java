
/*
meta:
  slug: sliding-window-maximum
  title: Sliding Window Maximum (Values)
  difficulty: medium
  tags: [deque, sliding-window]
  platform: custom
  link: null
  time: O(n)
  space: O(k)
question: Return max in each window of size k for an array.
approach: Monotonic deque (store indices) to track window maxima.
*/
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class MaxElementInSubArr {

    public static List<Integer> getMaxElements(List<Integer> nums, int k) {
        if (nums == null || nums.size() < k || k <= 0) {
            return new ArrayList<>();
        }

        List<Integer> maxValues = new ArrayList<>();
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i < nums.size(); i++) {
            // 1. Clean front: Remove indices that are out of the window.
            if (!deque.isEmpty() && deque.peekFirst() <= i - k) {
                deque.removeFirst();
            }

            // 2. Clean back: A simple while loop to remove all smaller elements.
            // This is the key part your code is missing.
            while (!deque.isEmpty() && nums.get(deque.peekLast()) < nums.get(i)) {
                deque.removeLast();
            }

            // 3. Add current index. This happens exactly once.
            deque.addLast(i);

            // 4. Record max once window is full. This happens last.
            if (i >= k - 1) {
                maxValues.add(nums.get(deque.peekFirst()));
            }
        }
        return maxValues;
    }

    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(1, 3, -1, -3, 5, 3, 6, 7));
        int k = 3;
        System.out.println(getMaxElements(nums, k)); // Correctly prints [3, 3, 5, 5, 6, 7]
    }
}