# Circular Buffer (Ring Buffer)

## Quick Definition

Fixed-size buffer with head and tail pointers that wrap around when reaching the end. Efficient for streaming data and producer-consumer scenarios.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Enqueue | **O(1)** | O(capacity) |
| Dequeue | **O(1)** | — |
| Peek | **O(1)** | — |
| Is Full/Empty | **O(1)** | — |

## Core Operations

```java
// Generic circular buffer implementation
class CircularBuffer<T> {
    private T[] buffer;
    private int head;     // points to first element
    private int tail;     // points to next insertion position
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public CircularBuffer(int capacity) {
        this.capacity = capacity;
        this.buffer = (T[]) new Object[capacity];
        this.head = 0;
        this.tail = 0;
        this.size = 0;
    }
    
    // Add element to buffer
    public boolean offer(T item) {
        if (isFull()) {
            return false;  // buffer full
        }
        buffer[tail] = item;
        tail = (tail + 1) % capacity;
        size++;
        return true;
    }
    
    // Add element, overwriting oldest if full
    public void put(T item) {
        buffer[tail] = item;
        tail = (tail + 1) % capacity;
        
        if (size < capacity) {
            size++;
        } else {
            head = (head + 1) % capacity;  // overwrite oldest
        }
    }
    
    // Remove and return front element
    public T poll() {
        if (isEmpty()) {
            return null;
        }
        T item = buffer[head];
        buffer[head] = null;  // help GC
        head = (head + 1) % capacity;
        size--;
        return item;
    }
    
    // Peek at front element without removing
    public T peek() {
        return isEmpty() ? null : buffer[head];
    }
    
    // Get element at index (0 = front)
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        return buffer[(head + index) % capacity];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
    public int capacity() { return capacity; }
    
    // Convert to array in order
    public T[] toArray() {
        @SuppressWarnings("unchecked")
        T[] result = (T[]) new Object[size];
        for (int i = 0; i < size; i++) {
            result[i] = get(i);
        }
        return result;
    }
}

// Specialized int circular buffer for performance
class IntCircularBuffer {
    private int[] buffer;
    private int head, tail, size, capacity;
    
    public IntCircularBuffer(int capacity) {
        this.capacity = capacity;
        this.buffer = new int[capacity];
        this.head = this.tail = this.size = 0;
    }
    
    public boolean offer(int value) {
        if (size == capacity) return false;
        buffer[tail] = value;
        tail = (tail + 1) % capacity;
        size++;
        return true;
    }
    
    public int poll() {
        if (size == 0) throw new RuntimeException("Buffer empty");
        int value = buffer[head];
        head = (head + 1) % capacity;
        size--;
        return value;
    }
    
    public int peek() {
        if (size == 0) throw new RuntimeException("Buffer empty");
        return buffer[head];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
}

// Producer-Consumer pattern with circular buffer
class ProducerConsumerBuffer<T> {
    private CircularBuffer<T> buffer;
    private final Object lock = new Object();
    
    public ProducerConsumerBuffer(int capacity) {
        buffer = new CircularBuffer<>(capacity);
    }
    
    public void produce(T item) throws InterruptedException {
        synchronized (lock) {
            while (buffer.isFull()) {
                lock.wait();  // wait for space
            }
            buffer.put(item);
            lock.notifyAll();  // notify consumers
        }
    }
    
    public T consume() throws InterruptedException {
        synchronized (lock) {
            while (buffer.isEmpty()) {
                lock.wait();  // wait for items
            }
            T item = buffer.poll();
            lock.notifyAll();  // notify producers
            return item;
        }
    }
}

// Moving average using circular buffer
class MovingAverage {
    private double[] buffer;
    private int head, size, capacity;
    private double sum;
    
    public MovingAverage(int capacity) {
        this.capacity = capacity;
        this.buffer = new double[capacity];
        this.head = 0;
        this.size = 0;
        this.sum = 0.0;
    }
    
    public double next(double val) {
        int index = (head + size) % capacity;
        
        if (size < capacity) {
            buffer[index] = val;
            sum += val;
            size++;
        } else {
            sum = sum - buffer[head] + val;  // replace oldest
            buffer[head] = val;
            head = (head + 1) % capacity;
        }
        
        return sum / size;
    }
}

// Usage examples
CircularBuffer<String> cb = new CircularBuffer<>(3);
cb.offer("A"); cb.offer("B"); cb.offer("C");
System.out.println(cb.poll());  // "A"
cb.offer("D");
System.out.println(Arrays.toString(cb.toArray()));  // [B, C, D]

// Moving average
MovingAverage ma = new MovingAverage(3);
System.out.println(ma.next(1));    // 1.0
System.out.println(ma.next(10));   // 5.5
System.out.println(ma.next(3));    // 4.67
System.out.println(ma.next(5));    // 6.0 (replaces 1)
```

## Python Snippet

```python
class CircularBuffer:
    def __init__(self, capacity):
        self.cap = capacity; self.buf = [None]*capacity
        self.head = 0; self.tail = 0; self.size = 0
    def offer(self, x):
        if self.size == self.cap: return False
        self.buf[self.tail] = x; self.tail = (self.tail+1) % self.cap; self.size += 1; return True
    def put(self, x):
        self.buf[self.tail] = x; self.tail = (self.tail+1) % self.cap
        if self.size < self.cap: self.size += 1
        else: self.head = (self.head+1) % self.cap
    def poll(self):
        if self.size == 0: return None
        x = self.buf[self.head]; self.buf[self.head] = None
        self.head = (self.head+1) % self.cap; self.size -= 1; return x
    def peek(self):
        return None if self.size == 0 else self.buf[self.head]

class MovingAverage:
    def __init__(self, k):
        self.k = k; self.buf = [0.0]*k; self.head = 0; self.size = 0; self.sum = 0.0
    def next(self, v):
        if self.size < self.k:
            self.buf[(self.head + self.size) % self.k] = v
            self.sum += v; self.size += 1
        else:
            self.sum -= self.buf[self.head]
            self.buf[self.head] = v
            self.sum += v; self.head = (self.head+1) % self.k
        return self.sum / self.size
```

## When to Use

- Audio/video streaming and real-time data processing
- Producer-consumer scenarios with bounded buffers
- Moving averages and sliding window calculations
- Network packet buffering
- Undo/redo functionality with size limits

## Trade-offs

**Pros:**

- O(1) all operations
- Fixed memory usage
- Cache-friendly sequential access
- Perfect for streaming data

**Cons:**

- Fixed capacity limitation
- Data loss if overwritten
- No dynamic resizing
- Complex index management

## Practice Problems

- **Moving Average from Data Stream**: Use circular buffer for efficiency
- **Design Hit Counter**: Circular buffer with timestamp tracking
- **Design Circular Queue**: Implement using array with head/tail pointers
- **Sliding Window Maximum**: Though deque is typically preferred
- **Rate Limiter**: Use circular buffer for request tracking

<details>
<summary>Implementation Notes (Advanced)</summary>

### Index Management

- **Modulo arithmetic**: head/tail wrapping with % operator
- **Power of 2 optimization**: Use bitwise AND for faster modulo
- **Size tracking**: Separate size variable vs calculating from head/tail
- **Full vs empty**: Distinguish using size or sentinel values

### Memory Considerations

- **Cache locality**: Sequential access patterns are cache-friendly
- **False sharing**: In multithreaded scenarios, pad head/tail to different cache lines
- **Memory layout**: Contiguous array provides better performance than linked structures

### Synchronization

- **Thread safety**: Requires careful synchronization for concurrent access
- **Lock-free**: Advanced implementations use atomic operations
- **Producer-consumer**: Blocking vs non-blocking variants

### Variations

- **Overwrite policy**: Overwrite oldest vs reject new items when full
- **Resizable**: Dynamic capacity adjustment (though rare)
- **Multi-producer/consumer**: Support multiple threads

</details>
