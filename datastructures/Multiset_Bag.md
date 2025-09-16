# Multiset (Bag)

## Quick Definition

Collection that allows duplicate elements and tracks their frequencies. Unlike sets, maintains count of each element occurrence.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Add | **O(1)** avg | O(n) |
| Remove | **O(1)** avg | — |
| Count | **O(1)** avg | — |
| Contains | **O(1)** avg | — |

## Core Operations

```java
// Manual implementation using Map<E, Integer>
class Multiset<E> {
    private Map<E, Integer> counts = new HashMap<>();
    private int totalSize = 0;
    
    public void add(E element) {
        counts.merge(element, 1, Integer::sum);
        totalSize++;
    }
    
    public void add(E element, int occurrences) {
        if (occurrences <= 0) return;
        counts.merge(element, occurrences, Integer::sum);
        totalSize += occurrences;
    }
    
    public boolean remove(E element) {
        Integer count = counts.get(element);
        if (count == null) return false;
        
        if (count == 1) {
            counts.remove(element);
        } else {
            counts.put(element, count - 1);
        }
        totalSize--;
        return true;
    }
    
    public int remove(E element, int occurrences) {
        Integer count = counts.get(element);
        if (count == null) return 0;
        
        int removed = Math.min(count, occurrences);
        if (count <= occurrences) {
            counts.remove(element);
        } else {
            counts.put(element, count - occurrences);
        }
        totalSize -= removed;
        return removed;
    }
    
    public int count(E element) {
        return counts.getOrDefault(element, 0);
    }
    
    public boolean contains(E element) {
        return counts.containsKey(element);
    }
    
    public int size() {
        return totalSize;
    }
    
    public Set<E> elementSet() {
        return counts.keySet();
    }
    
    public Collection<E> elements() {
        List<E> result = new ArrayList<>();
        for (Map.Entry<E, Integer> entry : counts.entrySet()) {
            for (int i = 0; i < entry.getValue(); i++) {
                result.add(entry.getKey());
            }
        }
        return result;
    }
    
    public Map<E, Integer> asMap() {
        return new HashMap<>(counts);
    }
}

// Using TreeMap for sorted multiset
class SortedMultiset<E> {
    private TreeMap<E, Integer> counts = new TreeMap<>();
    private int totalSize = 0;
    
    public SortedMultiset() {}
    
    public SortedMultiset(Comparator<E> comparator) {
        counts = new TreeMap<>(comparator);
    }
    
    public void add(E element) {
        counts.merge(element, 1, Integer::sum);
        totalSize++;
    }
    
    public E first() {
        return counts.isEmpty() ? null : counts.firstKey();
    }
    
    public E last() {
        return counts.isEmpty() ? null : counts.lastKey();
    }
    
    public NavigableSet<E> elementSet() {
        return counts.navigableKeySet();
    }
}

// Frequency analysis example
class FrequencyAnalyzer {
    public static Map<String, Integer> analyzeText(String text) {
        Multiset<String> wordCounts = new Multiset<>();
        String[] words = text.toLowerCase().split("\\W+");
        
        for (String word : words) {
            if (!word.isEmpty()) {
                wordCounts.add(word);
            }
        }
        
        return wordCounts.asMap();
    }
    
    public static List<Map.Entry<String, Integer>> getTopWords(String text, int k) {
        Map<String, Integer> frequencies = analyzeText(text);
        return frequencies.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .limit(k)
                .collect(Collectors.toList());
    }
}

// Character frequency counter
class CharacterCounter {
    private Multiset<Character> charCounts = new Multiset<>();
    
    public void addString(String str) {
        for (char c : str.toCharArray()) {
            charCounts.add(c);
        }
    }
    
    public boolean canFormPalindrome() {
        int oddCount = 0;
        for (char c : charCounts.elementSet()) {
            if (charCounts.count(c) % 2 == 1) {
                oddCount++;
            }
        }
        return oddCount <= 1;
    }
    
    public boolean isAnagram(String other) {
        Multiset<Character> otherCounts = new Multiset<>();
        for (char c : other.toCharArray()) {
            otherCounts.add(c);
        }
        return charCounts.asMap().equals(otherCounts.asMap());
    }
}

// Sliding window character frequency
class SlidingWindowMultiset {
    private Multiset<Character> window = new Multiset<>();
    private int distinctCount = 0;
    
    public void addChar(char c) {
        if (window.count(c) == 0) {
            distinctCount++;
        }
        window.add(c);
    }
    
    public void removeChar(char c) {
        window.remove(c);
        if (window.count(c) == 0) {
            distinctCount--;
        }
    }
    
    public int getDistinctCount() {
        return distinctCount;
    }
    
    public boolean hasExactlyKDistinct(int k) {
        return distinctCount == k;
    }
}

// Usage examples
Multiset<String> bag = new Multiset<>();
bag.add("apple");
bag.add("banana");
bag.add("apple");  // allows duplicates
System.out.println(bag.count("apple"));  // 2
System.out.println(bag.size());          // 3

// Character frequency
CharacterCounter counter = new CharacterCounter();
counter.addString("listen");
counter.addString("silent");
System.out.println(counter.isAnagram("listen")); // true
```

## Python Snippet

```python
from collections import Counter

class Multiset:
    def __init__(self): self.c = Counter(); self.total = 0
    def add(self, x, k=1): self.c[x] += k; self.total += k
    def remove(self, x, k=1):
        r = min(k, self.c.get(x, 0)); self.c[x] -= r
        if self.c[x] <= 0: self.c.pop(x, None)
        self.total -= r; return r
    def count(self, x): return self.c.get(x, 0)
    def contains(self, x): return x in self.c
    def size(self): return self.total
    def elements(self):
        for x, n in self.c.items():
            for _ in range(n): yield x

def analyze_text(text):
    words = [w for w in ''.join(ch.lower() if ch.isalnum() else ' ' for ch in text).split() if w]
    return Counter(words)
```

## When to Use

- Frequency counting and analysis
- Anagram detection and word puzzles
- Statistical analysis of data
- Character/element frequency tracking
- Bag-based algorithms

## Trade-offs

**Pros:**

- Natural frequency tracking
- Efficient add/remove operations
- Rich querying capabilities
- Can be sorted or unsorted

**Cons:**

- Higher memory overhead than simple sets
- More complex than basic collections
- Iteration includes duplicates
- No standard library implementation

## Practice Problems

- **Valid Anagram**: Character frequency comparison
- **Group Anagrams**: Multiset-based grouping
- **Minimum Window Substring**: Sliding window with character counts
- **Find All Anagrams in String**: Character frequency matching
- **Top K Frequent Elements**: Frequency analysis

<details>
<summary>Implementation Notes (Advanced)</summary>

### Storage Strategies

- **HashMap**: Fast operations, no ordering
- **TreeMap**: Sorted elements, slower operations
- **Array**: For limited alphabet (characters, digits)
- **Counter array**: Fixed-size alphabet optimization

### Memory Optimization

- **Sparse representation**: Only store non-zero counts
- **Bit manipulation**: For small count values
- **Primitive collections**: Avoid boxing overhead
- **Custom hash functions**: Optimize for specific data

### Performance Considerations

- **Iteration patterns**: Count-based vs element-based
- **Bulk operations**: Batch processing for efficiency
- **Memory access**: Locality considerations for large datasets

</details>
