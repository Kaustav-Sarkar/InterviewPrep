# Cartesian Tree

## Quick Definition

Binary tree built from array where in-order traversal gives original sequence and each node satisfies heap property with respect to parent. Combines sequence order with priority-based structure.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Build | **O(n)** | O(n) |
| Range Min Query | **O(1)** | — |
| Lowest Common Ancestor | **O(1)** | — |
| Insert (dynamic) | O(log n) | — |
| Delete (dynamic) | O(log n) | — |

## Core Operations

```java
class CartesianNode {
    int value;
    int index;  // original position in array
    CartesianNode left, right, parent;
    
    public CartesianNode(int value, int index) {
        this.value = value;
        this.index = index;
    }
}

class CartesianTree {
    private CartesianNode root;
    private int[] array;
    
    public CartesianTree(int[] arr) {
        this.array = arr.clone();
        this.root = buildCartesianTree(arr);
    }
    
    // Build Cartesian tree from array in O(n) time using stack
    private CartesianNode buildCartesianTree(int[] arr) {
        if (arr.length == 0) return null;
        
        Deque<CartesianNode> stack = new ArrayDeque<>();
        
        for (int i = 0; i < arr.length; i++) {
            CartesianNode current = new CartesianNode(arr[i], i);
            CartesianNode lastPopped = null;
            
            // Pop elements while current value is smaller
            while (!stack.isEmpty() && stack.peek().value > current.value) {
                lastPopped = stack.pop();
            }
            
            if (lastPopped != null) {
                current.left = lastPopped;
            }
            
            if (!stack.isEmpty()) {
                stack.peek().right = current;
            }
            
            stack.push(current);
        }
        
        // Find root (leftmost element in stack)
        return stack.peekFirst();
    }
    
    // Range Minimum Query in O(1) after preprocessing
    public int rangeMinQuery(int left, int right) {
        CartesianNode lcaNode = findLCA(left, right);
        return lcaNode.value;
    }
}

// Usage example
int[] array = {3, 2, 6, 1, 9, 7, 5};
CartesianTree ct = new CartesianTree(array);

System.out.println("RMQ(0, 3): " + ct.rangeMinQuery(0, 3)); // min(3,2,6,1) = 1
System.out.println("RMQ(2, 5): " + ct.rangeMinQuery(2, 5)); // min(6,1,9,7) = 1
```

## Python Snippet

```python
from collections import deque

class Node:
    def __init__(self, val, idx):
        self.val = val; self.idx = idx; self.left = None; self.right = None

def build_cartesian(arr):
    st, last = [], None
    for i, v in enumerate(arr):
        curr, last = Node(v, i), None
        while st and st[-1].val > v:
            last = st.pop()
        if last: curr.left = last
        if st: st[-1].right = curr
        st.append(curr)
    return st[0] if st else None
```

## When to Use

- Range minimum/maximum query preprocessing
- Lowest Common Ancestor queries
- Building other tree structures (Treaps)
- Suffix arrays and string algorithms
- Computational geometry applications

## Trade-offs

**Pros:**

- Linear time construction O(n)
- Constant time RMQ after preprocessing
- Preserves array sequence in in-order traversal
- Natural LCA structure
- Fundamental building block for other structures

**Cons:**

- Limited to static arrays (for basic version)
- More complex than direct RMQ approaches
- Not always intuitive to construct
- Memory overhead for tree structure
- Mainly useful for specific algorithmic problems

## Practice Problems

- **Range Minimum Query**: Static RMQ with Cartesian trees
- **Lowest Common Ancestor**: Tree LCA queries
- **Largest Rectangle in Histogram**: Using Cartesian tree structure
- **Maximal Rectangle**: 2D extension of histogram problem
- **Binary Tree from Array**: Construct tree maintaining properties

<details>
<summary>Implementation Notes (Advanced)</summary>

### Construction Algorithm

- **Stack-based**: O(n) construction using monotonic stack
- **Recursive approach**: Divide-and-conquer O(n log n) method
- **Properties maintenance**: Ensure heap and sequence properties
- **Index tracking**: Maintain original array positions

### Range Minimum Query

- **LCA reduction**: RMQ reduces to LCA on Cartesian tree
- **Constant time**: After O(n) preprocessing
- **Space tradeoffs**: Tree storage vs lookup tables
- **Query optimization**: Efficient LCA algorithms

### Applications in Algorithms

- **Suffix arrays**: Used in suffix tree construction
- **String matching**: Pattern matching algorithms
- **Computational geometry**: Range queries on points
- **Data compression**: Structural properties for encoding

### Comparison with Alternatives

- **vs Sparse Table**: Cartesian tree + LCA vs direct sparse table
- **vs Segment Tree**: Static vs dynamic scenarios
- **vs Fenwick Tree**: Min queries vs sum queries
- **Memory usage**: Tree structure vs table storage

</details>
