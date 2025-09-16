# KD-Tree

## Quick Definition

Binary tree that partitions k-dimensional space by alternating split dimensions at each level. Efficiently organizes points for spatial queries like nearest neighbor and range search.

## Big-O Summary

| Operation | Time (Average) | Time (Worst) | Space |
|-----------|----------------|--------------|-------|
| Build | **O(n log n)** | O(n log n) | O(n) |
| Search | **O(log n)** | O(n) | — |
| Insert | **O(log n)** | O(n) | — |
| k-NN | O(log n + k) | O(n) | — |
| Range Query | O(log n + m) | O(n) | — |

*m = number of points in range*

## Core Operations

```java
class Point {
    double[] coords;
    
    public Point(double... coords) {
        this.coords = coords.clone();
    }
    
    public double get(int dimension) {
        return coords[dimension];
    }
    
    public int getDimensions() {
        return coords.length;
    }
    
    public double distanceTo(Point other) {
        double sum = 0;
        for (int i = 0; i < coords.length; i++) {
            double diff = coords[i] - other.coords[i];
            sum += diff * diff;
        }
        return Math.sqrt(sum);
    }
    
    @Override
    public String toString() {
        return Arrays.toString(coords);
    }
}

class KDNode {
    Point point;
    KDNode left, right;
    int splitDimension;
    
    public KDNode(Point point, int splitDimension) {
        this.point = point;
        this.splitDimension = splitDimension;
        this.left = this.right = null;
    }
}

class KDTree {
    private KDNode root;
    private int dimensions;
    
    public KDTree(int dimensions) {
        this.dimensions = dimensions;
        this.root = null;
    }
    
    public void insert(Point point) {
        root = insertHelper(root, point, 0);
    }
    
    private KDNode insertHelper(KDNode node, Point point, int depth) {
        if (node == null) {
            return new KDNode(point, depth % dimensions);
        }
        
        int splitDim = depth % dimensions;
        
        if (point.get(splitDim) < node.point.get(splitDim)) {
            node.left = insertHelper(node.left, point, depth + 1);
        } else {
            node.right = insertHelper(node.right, point, depth + 1);
        }
        
        return node;
    }
    
    // Build tree from array of points (more efficient)
    public static KDTree buildTree(Point[] points, int dimensions) {
        KDTree tree = new KDTree(dimensions);
        tree.root = tree.buildHelper(points, 0);
        return tree;
    }
    
    private KDNode buildHelper(Point[] points, int depth) {
        if (points.length == 0) return null;
        
        int splitDim = depth % dimensions;
        
        // Sort points by current dimension
        Arrays.sort(points, (a, b) -> Double.compare(a.get(splitDim), b.get(splitDim)));
        
        int median = points.length / 2;
        KDNode node = new KDNode(points[median], splitDim);
        
        // Recursively build left and right subtrees
        Point[] leftPoints = Arrays.copyOfRange(points, 0, median);
        Point[] rightPoints = Arrays.copyOfRange(points, median + 1, points.length);
        
        node.left = buildHelper(leftPoints, depth + 1);
        node.right = buildHelper(rightPoints, depth + 1);
        
        return node;
    }
    
    // Find nearest neighbor
    public Point nearestNeighbor(Point target) {
        if (root == null) return null;
        return nearestHelper(root, target, root.point, Double.MAX_VALUE).point;
    }
    
    private BestMatch nearestHelper(KDNode node, Point target, Point best, double bestDist) {
        if (node == null) {
            return new BestMatch(best, bestDist);
        }
        
        // Check if current node is closer
        double dist = node.point.distanceTo(target);
        if (dist < bestDist) {
            best = node.point;
            bestDist = dist;
        }
        
        int splitDim = node.splitDimension;
        double diff = target.get(splitDim) - node.point.get(splitDim);
        
        // Choose which side to explore first
        KDNode firstSide = diff < 0 ? node.left : node.right;
        KDNode secondSide = diff < 0 ? node.right : node.left;
        
        // Explore first side
        BestMatch result = nearestHelper(firstSide, target, best, bestDist);
        
        // Check if we need to explore second side
        if (Math.abs(diff) < result.distance) {
            result = nearestHelper(secondSide, target, result.point, result.distance);
        }
        
        return result;
    }
    
    private static class BestMatch {
        Point point;
        double distance;
        
        BestMatch(Point point, double distance) {
            this.point = point;
            this.distance = distance;
        }
    }
    
    // Range search
    public List<Point> rangeSearch(Point min, Point max) {
        List<Point> result = new ArrayList<>();
        rangeSearchHelper(root, min, max, result);
        return result;
    }
    
    private void rangeSearchHelper(KDNode node, Point min, Point max, List<Point> result) {
        if (node == null) return;
        
        // Check if current point is in range
        boolean inRange = true;
        for (int i = 0; i < dimensions; i++) {
            if (node.point.get(i) < min.get(i) || node.point.get(i) > max.get(i)) {
                inRange = false;
                break;
            }
        }
        
        if (inRange) {
            result.add(node.point);
        }
        
        int splitDim = node.splitDimension;
        
        // Check left subtree
        if (min.get(splitDim) <= node.point.get(splitDim)) {
            rangeSearchHelper(node.left, min, max, result);
        }
        
        // Check right subtree
        if (max.get(splitDim) >= node.point.get(splitDim)) {
            rangeSearchHelper(node.right, min, max, result);
        }
    }
    
    // k-nearest neighbors
    public List<Point> kNearestNeighbors(Point target, int k) {
        PriorityQueue<PointDistance> maxHeap = new PriorityQueue<>(
            (a, b) -> Double.compare(b.distance, a.distance)
        );
        
        kNearestHelper(root, target, k, maxHeap);
        
        List<Point> result = new ArrayList<>();
        while (!maxHeap.isEmpty()) {
            result.add(0, maxHeap.poll().point); // Add to front for correct order
        }
        return result;
    }
    
    private void kNearestHelper(KDNode node, Point target, int k, PriorityQueue<PointDistance> maxHeap) {
        if (node == null) return;
        
        double dist = node.point.distanceTo(target);
        
        if (maxHeap.size() < k) {
            maxHeap.offer(new PointDistance(node.point, dist));
        } else if (dist < maxHeap.peek().distance) {
            maxHeap.poll();
            maxHeap.offer(new PointDistance(node.point, dist));
        }
        
        int splitDim = node.splitDimension;
        double diff = target.get(splitDim) - node.point.get(splitDim);
        
        // Visit closer side first
        KDNode firstSide = diff < 0 ? node.left : node.right;
        KDNode secondSide = diff < 0 ? node.right : node.left;
        
        kNearestHelper(firstSide, target, k, maxHeap);
        
        // Check if we need to visit other side
        if (maxHeap.size() < k || Math.abs(diff) < maxHeap.peek().distance) {
            kNearestHelper(secondSide, target, k, maxHeap);
        }
    }
    
    private static class PointDistance {
        Point point;
        double distance;
        
        PointDistance(Point point, double distance) {
            this.point = point;
            this.distance = distance;
        }
    }
}

// 2D-specific implementation for efficiency
class KDTree2D {
    private TreeSet<Point> xSorted, ySorted;
    
    public KDTree2D() {
        xSorted = new TreeSet<>((a, b) -> Double.compare(a.get(0), b.get(0)));
        ySorted = new TreeSet<>((a, b) -> Double.compare(a.get(1), b.get(1)));
    }
    
    public void insert(Point point) {
        xSorted.add(point);
        ySorted.add(point);
    }
    
    public List<Point> rangeSearch(double xMin, double yMin, double xMax, double yMax) {
        Point min = new Point(xMin, yMin);
        Point max = new Point(xMax, yMax);
        
        NavigableSet<Point> xRange = xSorted.subSet(min, true, max, true);
        
        return xRange.stream()
                     .filter(p -> p.get(1) >= yMin && p.get(1) <= yMax)
                     .collect(Collectors.toList());
    }
}

// Usage examples
// Build KD-Tree
Point[] points = {
    new Point(2, 3), new Point(5, 4), new Point(9, 6),
    new Point(4, 7), new Point(8, 1), new Point(7, 2)
};

KDTree kdTree = KDTree.buildTree(points, 2);

// Nearest neighbor search
Point target = new Point(6, 5);
Point nearest = kdTree.nearestNeighbor(target);
System.out.println("Nearest to " + target + " is " + nearest);

// k-nearest neighbors
List<Point> kNearest = kdTree.kNearestNeighbors(target, 3);
System.out.println("3 nearest neighbors: " + kNearest);

// Range search
Point min = new Point(3, 2);
Point max = new Point(8, 6);
List<Point> inRange = kdTree.rangeSearch(min, max);
System.out.println("Points in range [" + min + ", " + max + "]: " + inRange);

// 2D specific usage
KDTree2D kdTree2D = new KDTree2D();
for (Point p : points) {
    kdTree2D.insert(p);
}

List<Point> rangeResult = kdTree2D.rangeSearch(3, 2, 8, 6);
System.out.println("2D range search result: " + rangeResult);
```

## Python Snippet

```python
import math, heapq

class Point:
    def __init__(self, *coords): self.coords = tuple(coords)
    def __getitem__(self, i): return self.coords[i]
    def __len__(self): return len(self.coords)
    def dist2(self, other):
        return sum((a-b)*(a-b) for a, b in zip(self.coords, other.coords))

class KDNode:
    def __init__(self, p, dim):
        self.p = p; self.dim = dim; self.left = None; self.right = None

class KDTree:
    def __init__(self, points, k):
        self.k = k
        self.root = self._build(points, 0)
    def _build(self, pts, depth):
        if not pts: return None
        d = depth % self.k
        pts.sort(key=lambda pt: pt[d])
        m = len(pts)//2
        node = KDNode(pts[m], d)
        node.left = self._build(pts[:m], depth+1)
        node.right = self._build(pts[m+1:], depth+1)
        return node
    def nearest(self, target):
        best = [None, float('inf')]
        def dfs(n):
            if not n: return
            dist = target.dist2(n.p)
            if dist < best[1]: best[0], best[1] = n.p, dist
            diff = target[n.dim] - n.p[n.dim]
            first, second = (n.left, n.right) if diff < 0 else (n.right, n.left)
            dfs(first)
            if diff*diff < best[1]: dfs(second)
        dfs(self.root); return best[0]
```

## When to Use

- Nearest neighbor search in low dimensions (≤10)
- Spatial indexing for geographic information systems
- Computer graphics and collision detection
- Machine learning k-NN algorithms
- Range queries on multidimensional data

## Trade-offs

**Pros:**

- Efficient for low-dimensional spaces
- Good for nearest neighbor and range queries
- Memory efficient compared to grid-based approaches
- Supports dynamic insertion
- Natural recursive structure

**Cons:**

- Performance degrades with high dimensions (curse of dimensionality)
- Can become unbalanced with poor insertion order
- Complex deletion implementation
- Not suitable for dimensions > 10-20

## Practice Problems

- **Closest Pair**: Find two closest points efficiently
- **K Nearest Neighbors**: Machine learning classification
- **Range Search**: Find points within rectangle/sphere
- **Geographic Queries**: Location-based services
- **Collision Detection**: Gaming and physics simulations

<details>
<summary>Implementation Notes (Advanced)</summary>

### Curse of Dimensionality

- **High dimensions**: Performance approaches linear search
- **Rule of thumb**: Effective for dimensions ≤ 10
- **Alternative**: Use LSH or approximate methods for high dimensions
- **Space partitioning**: Becomes less effective as dimensions increase

### Tree Construction

- **Balanced construction**: Sort points and choose median
- **Dimension cycling**: Round-robin through dimensions
- **Median finding**: Can use quick-select for efficiency
- **Bulk loading**: More efficient than repeated insertion

### Query Optimization

- **Pruning**: Skip subtrees that can't contain better solutions
- **Priority search**: Explore most promising branches first
- **Bounding boxes**: Precompute bounds for faster pruning
- **Approximate queries**: Trade accuracy for speed

### Memory Layout

- **Cache locality**: Consider memory-friendly layouts
- **Node packing**: Store multiple nodes in arrays
- **Implicit trees**: Array-based representation
- **Memory pools**: Reduce allocation overhead

</details>
