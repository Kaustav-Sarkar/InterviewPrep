package CommonQuestions;

import java.util.HashMap;
import java.util.Map;

public class LRUCache {
    private int capacity;
    private Map<Integer, Node> cache; // map will contain key and Node
    private Node mostRecentlyUsed;
    private Node leastRecentlyUsed;

    LRUCache(int capacity) {
        this.cache = new HashMap<>();
        this.capacity = capacity;
        this.mostRecentlyUsed = new Node(-1, -1);
        this.leastRecentlyUsed = new Node(-1, -1);
        mostRecentlyUsed.next = leastRecentlyUsed;
        leastRecentlyUsed.prev = mostRecentlyUsed;
        mostRecentlyUsed.prev = null;
        leastRecentlyUsed.next = null;
    }

    public class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    public void removeNode(Node node) {
        Node nextNode = node.next;
        Node prevNode = node.prev;
        prevNode.next = nextNode;
        nextNode.prev = prevNode;
    }

    public void updateNode(Node node, int value) {
        node.value = value;
        removeNode(node);
        addFirst(node);
    }

    public void removeLastNode() {
        removeNode(leastRecentlyUsed.prev);
    }

    public void addFirst(Node node) {
        Node nextNode = mostRecentlyUsed.next;
        nextNode.prev = node;
        mostRecentlyUsed.next = node;
        node.prev = mostRecentlyUsed;
        node.next = nextNode;
    }

    public void addLast(Node node) {
        Node prevNode = leastRecentlyUsed.prev;
        node.next = leastRecentlyUsed;
        node.prev = prevNode;
        prevNode.next = node;
        leastRecentlyUsed.prev = node;
    }

    public Integer get(Integer key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        Node node = cache.get(key);
        removeNode(node);
        addFirst(node);
        return node.value;
    }

    public Integer put(Integer key, Integer value) {
        if (cache.containsKey(key)) {
            System.out.println("already exists, updating to new value");
            return update(key, value);
        }
        Node newNode = new Node(key, value);
        if (cache.size() == capacity) {
            int keytoRemove = leastRecentlyUsed.prev.key;
            removeLastNode();
            cache.remove(keytoRemove); // remove from cache as well
            addFirst(newNode);
            cache.put(key, newNode);
        } else {
            addFirst(newNode);
            cache.put(key, newNode);
        }
        return value;
    }

    public Integer update(Integer key, Integer value) {
        if (!cache.containsKey(key)) {
            System.out.println("doesnt exists, creating new node");
            return put(key, value);
        }
        Node existingNode = cache.get(key);
        updateNode(existingNode, value);
        return value;
    }

    public static void main(String[] args) {
        testCacheOfSize2(); // The original test case
        testCacheOfSize1(); // A tricky edge case
        testCacheOfSize3(); // A larger test case
    }

    // Test case for a cache with capacity = 2
    public static void testCacheOfSize2() {
        System.out.println("--- Starting Test: Cache with Capacity 2 ---");
        LRUCache lruCache = new LRUCache(2);
        lruCache.put(1, 10);
        lruCache.put(2, 20);
        lruCache.printCacheState("put(2, 20)"); // Expected: {1=10, 2=20}

        lruCache.get(1);
        lruCache.printCacheState("get(1)"); // Expected: {2=20, 1=10} (Order in map might vary)

        lruCache.put(3, 30); // Evicts key 2
        lruCache.printCacheState("put(3, 30)"); // Expected: {1=10, 3=30}

        int val = lruCache.get(2);
        System.out.println("get(2) returned: " + val); // Expected: -1
        System.out.println("--- Test Complete: Capacity 2 ---\n");
    }

    // Test case for the edge case of capacity = 1
    public static void testCacheOfSize1() {
        System.out.println("--- Starting Test: Cache with Capacity 1 ---");
        LRUCache lruCache = new LRUCache(1);

        lruCache.put(1, 10);
        lruCache.printCacheState("put(1, 10)"); // Expected: {1=10}

        lruCache.put(2, 20); // Evicts key 1
        lruCache.printCacheState("put(2, 20)"); // Expected: {2=20}

        int val1 = lruCache.get(1);
        System.out.println("get(1) returned: " + val1); // Expected: -1

        int val2 = lruCache.get(2);
        System.out.println("get(2) returned: " + val2); // Expected: 20
        lruCache.printCacheState("get(2)"); // Expected: {2=20}
        System.out.println("--- Test Complete: Capacity 1 ---\n");
    }

    // Test case for a larger cache with capacity = 3
    public static void testCacheOfSize3() {
        System.out.println("--- Starting Test: Cache with Capacity 3 ---");
        LRUCache lruCache = new LRUCache(3);

        lruCache.put(1, 10);
        lruCache.put(2, 20);
        lruCache.put(3, 30);
        lruCache.printCacheState("put(3, 30)"); // Expected: {1=10, 2=20, 3=30}

        lruCache.put(4, 40); // Evicts key 1 (the LRU)
        lruCache.printCacheState("put(4, 40)"); // Expected: {2=20, 3=30, 4=40}

        lruCache.get(2); // Access key 2, making it the most recently used
        lruCache.printCacheState("get(2)"); // Order in map may vary, but 3 is now LRU

        lruCache.put(5, 50); // Evicts key 3 (the new LRU)
        lruCache.printCacheState("put(5, 50)"); // Expected: {2=20, 4=40, 5=50}

        int val = lruCache.get(3);
        System.out.println("get(3) returned: " + val); // Expected: -1
        System.out.println("--- Test Complete: Capacity 3 ---\n");
    }

    // Helper method to print the current state of the cache for verification
    public void printCacheState(String operation) {
        System.out.print("After " + operation + " -> Cache state: {");
        for (Map.Entry<Integer, Node> entry : cache.entrySet()) {
            System.out.print(entry.getKey() + "=" + entry.getValue().value + " ");
        }
        System.out.println("}");
    }
}
