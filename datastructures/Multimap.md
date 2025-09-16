# Multimap

## Quick Definition

Map where each key can be associated with multiple values. Allows one-to-many relationships and duplicate key-value pairs.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Put | **O(1)** avg | O(n) |
| Get Values | **O(1)** avg | — |
| Remove | **O(1)** avg | — |
| Contains | **O(1)** avg | — |

## Core Operations

```java
// Manual implementation using Map<K, List<V>>
class Multimap<K, V> {
    private Map<K, List<V>> map = new HashMap<>();
    
    public void put(K key, V value) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }
    
    public List<V> get(K key) {
        return map.getOrDefault(key, Collections.emptyList());
    }
    
    public boolean remove(K key, V value) {
        List<V> values = map.get(key);
        if (values != null && values.remove(value)) {
            if (values.isEmpty()) {
                map.remove(key);
            }
            return true;
        }
        return false;
    }
    
    public boolean containsEntry(K key, V value) {
        List<V> values = map.get(key);
        return values != null && values.contains(value);
    }
    
    public Set<K> keySet() {
        return map.keySet();
    }
    
    public int size() {
        return map.values().stream().mapToInt(List::size).sum();
    }
}

// Group anagrams example
Map<String, List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> multimap = new HashMap<>();
    
    for (String str : strs) {
        char[] chars = str.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);
        
        multimap.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
    }
    
    return multimap;
}

// Inverted index for text search
class InvertedIndex {
    private Map<String, Set<Integer>> wordToDocuments = new HashMap<>();
    
    public void addDocument(int docId, String[] words) {
        for (String word : words) {
            wordToDocuments.computeIfAbsent(word.toLowerCase(), 
                k -> new HashSet<>()).add(docId);
        }
    }
    
    public Set<Integer> search(String word) {
        return wordToDocuments.getOrDefault(word.toLowerCase(), 
                                           Collections.emptySet());
    }
}

// Graph adjacency list
class Graph {
    private Map<Integer, List<Integer>> adjacencyList = new HashMap<>();
    
    public void addEdge(int from, int to) {
        adjacencyList.computeIfAbsent(from, k -> new ArrayList<>()).add(to);
    }
    
    public List<Integer> getNeighbors(int vertex) {
        return adjacencyList.getOrDefault(vertex, Collections.emptyList());
    }
}

// Category management
class CategoryManager<T> {
    private Map<String, List<T>> categories = new HashMap<>();
    
    public void addItem(String category, T item) {
        categories.computeIfAbsent(category, k -> new ArrayList<>()).add(item);
    }
    
    public List<T> getItemsInCategory(String category) {
        return new ArrayList<>(categories.getOrDefault(category, Collections.emptyList()));
    }
}

// Usage examples
Multimap<String, Integer> multimap = new Multimap<>();
multimap.put("fruits", 1);
multimap.put("fruits", 2);
System.out.println(multimap.get("fruits"));  // [1, 2]

// Group anagrams
String[] words = {"eat", "tea", "tan", "ate", "nat", "bat"};
Map<String, List<String>> grouped = groupAnagrams(words);
```

## Python Snippet

```python
from collections import defaultdict

class Multimap:
    def __init__(self): self.m = defaultdict(list)
    def put(self, k, v): self.m[k].append(v)
    def get(self, k): return list(self.m.get(k, ()))
    def remove(self, k, v):
        lst = self.m.get(k); 
        if not lst: return False
        try:
            lst.remove(v)
            if not lst: del self.m[k]
            return True
        except ValueError:
            return False

def group_anagrams(strs):
    mm = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        mm[key].append(s)
    return dict(mm)
```

## When to Use

- Group anagrams or similar word/string problems
- Inverted indexes for search engines
- Graph adjacency list representations
- Category-based data organization
- One-to-many relationship modeling

## Trade-offs

**Pros:**

- Natural modeling of one-to-many relationships
- Flexible value collection types (List, Set)
- Efficient for grouping operations
- Easy to implement with standard collections

**Cons:**

- Higher memory overhead than simple maps
- More complex iteration patterns
- Potential for empty collections
- Not part of standard Java collections

## Practice Problems

- **Group Anagrams**: Classic multimap application
- **Letter Combinations**: Phone number to letter mappings
- **Word Pattern**: Map characters to words
- **Employee Free Time**: Group intervals by employee
- **Design Search Autocomplete**: Prefix to word suggestions

<details>
<summary>Implementation Notes (Advanced)</summary>

### Collection Choice

- **ArrayList**: Allows duplicates, maintains insertion order
- **HashSet**: No duplicates, no order guarantees
- **TreeSet**: No duplicates, sorted order
- **LinkedHashSet**: No duplicates, insertion order

### Memory Management

- **Empty collections**: Remove keys when collections become empty
- **Memory overhead**: Each collection has its own overhead
- **Lazy initialization**: Create collections only when needed

### Performance Considerations

- **Iteration**: Flattening all values can be expensive
- **Size calculation**: May require iterating all collections
- **Bulk operations**: Consider batch processing for efficiency

</details>
