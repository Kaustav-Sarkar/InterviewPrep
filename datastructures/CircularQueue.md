# Circular Queue

## Quick Definition

Queue implementation using fixed-size array where rear wraps around to front when reaching end. Efficiently uses space with constant-time operations.

## Big-O Summary

| Operation | Time | Space |
|-----------|------|-------|
| Enqueue | **O(1)** | O(capacity) |
| Dequeue | **O(1)** | — |
| Peek | **O(1)** | — |
| Is Full/Empty | **O(1)** | — |

## Core Operations

```java
class CircularQueue {
    private int[] queue;
    private int front;
    private int rear;
    private int size;
    private int capacity;
    
    public CircularQueue(int capacity) {
        this.capacity = capacity;
        this.queue = new int[capacity];
        this.front = 0;
        this.rear = -1;
        this.size = 0;
    }
    
    public boolean enqueue(int item) {
        if (isFull()) {
            return false;
        }
        
        rear = (rear + 1) % capacity;
        queue[rear] = item;
        size++;
        return true;
    }
    
    public Integer dequeue() {
        if (isEmpty()) {
            return null;
        }
        
        int item = queue[front];
        front = (front + 1) % capacity;
        size--;
        return item;
    }
    
    public Integer peek() {
        return isEmpty() ? null : queue[front];
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
    
    public boolean isFull() {
        return size == capacity;
    }
    
    public int size() {
        return size;
    }
    
    // Display queue contents
    public String toString() {
        if (isEmpty()) return "[]";
        
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < size; i++) {
            int index = (front + i) % capacity;
            sb.append(queue[index]);
            if (i < size - 1) sb.append(", ");
        }
        return sb.append("]").toString();
    }
}

// Generic circular queue
class GenericCircularQueue<T> {
    private T[] queue;
    private int front;
    private int rear;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public GenericCircularQueue(int capacity) {
        this.capacity = capacity;
        this.queue = (T[]) new Object[capacity];
        this.front = 0;
        this.rear = -1;
        this.size = 0;
    }
    
    public boolean offer(T item) {
        if (isFull()) return false;
        
        rear = (rear + 1) % capacity;
        queue[rear] = item;
        size++;
        return true;
    }
    
    public T poll() {
        if (isEmpty()) return null;
        
        T item = queue[front];
        queue[front] = null;  // help GC
        front = (front + 1) % capacity;
        size--;
        return item;
    }
    
    public T peek() {
        return isEmpty() ? null : queue[front];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
}

// Round-robin scheduler
class RoundRobinScheduler {
    private CircularQueue processes;
    private int timeQuantum;
    
    public RoundRobinScheduler(int maxProcesses, int timeQuantum) {
        this.processes = new CircularQueue(maxProcesses);
        this.timeQuantum = timeQuantum;
    }
    
    public void addProcess(int processId) {
        if (!processes.enqueue(processId)) {
            System.out.println("Process queue full!");
        }
    }
    
    public int getNextProcess() {
        Integer process = processes.dequeue();
        if (process != null) {
            // Re-add to end for round-robin
            processes.enqueue(process);
        }
        return process != null ? process : -1;
    }
    
    public void executeRound() {
        if (!processes.isEmpty()) {
            int currentProcess = getNextProcess();
            System.out.println("Executing process " + currentProcess + 
                             " for " + timeQuantum + " ms");
        }
    }
}

// Producer-Consumer with circular queue
class ProducerConsumer {
    private GenericCircularQueue<String> buffer;
    private final Object lock = new Object();
    
    public ProducerConsumer(int bufferSize) {
        buffer = new GenericCircularQueue<>(bufferSize);
    }
    
    public void produce(String item) throws InterruptedException {
        synchronized (lock) {
            while (buffer.isFull()) {
                lock.wait();
            }
            buffer.offer(item);
            System.out.println("Produced: " + item);
            lock.notifyAll();
        }
    }
    
    public String consume() throws InterruptedException {
        synchronized (lock) {
            while (buffer.isEmpty()) {
                lock.wait();
            }
            String item = buffer.poll();
            System.out.println("Consumed: " + item);
            lock.notifyAll();
            return item;
        }
    }
}

// Print queue using circular queue
class PrintQueue {
    private GenericCircularQueue<String> jobs;
    
    public PrintQueue(int capacity) {
        jobs = new GenericCircularQueue<>(capacity);
    }
    
    public boolean addJob(String document) {
        return jobs.offer(document);
    }
    
    public String printNext() {
        String job = jobs.poll();
        if (job != null) {
            System.out.println("Printing: " + job);
        }
        return job;
    }
    
    public int getPendingJobs() {
        return jobs.size();
    }
    
    public boolean isEmpty() {
        return jobs.isEmpty();
    }
}

// Usage examples
CircularQueue cq = new CircularQueue(5);
cq.enqueue(10); cq.enqueue(20); cq.enqueue(30);
System.out.println(cq);          // [10, 20, 30]
System.out.println(cq.dequeue()); // 10
cq.enqueue(40); cq.enqueue(50);
System.out.println(cq);          // [20, 30, 40, 50]

// Round-robin example
RoundRobinScheduler scheduler = new RoundRobinScheduler(3, 100);
scheduler.addProcess(1);
scheduler.addProcess(2);
scheduler.addProcess(3);
scheduler.executeRound();  // Process 1
scheduler.executeRound();  // Process 2
scheduler.executeRound();  // Process 3
```

## Python Snippet

```python
class CircularQueue:
    def __init__(self, capacity):
        self.cap = capacity; self.a = [0]*capacity
        self.front = 0; self.rear = -1; self.size = 0
    def enqueue(self, x):
        if self.size == self.cap: return False
        self.rear = (self.rear + 1) % self.cap
        self.a[self.rear] = x; self.size += 1; return True
    def dequeue(self):
        if self.size == 0: return None
        x = self.a[self.front]
        self.front = (self.front + 1) % self.cap; self.size -= 1; return x
    def peek(self):
        return None if self.size == 0 else self.a[self.front]
    def is_empty(self): return self.size == 0
    def is_full(self): return self.size == self.cap
```

## When to Use

- Round-robin scheduling algorithms
- Producer-consumer scenarios with bounded buffers
- Print job queues and task scheduling
- Fixed-size streaming data buffers
- Traffic control and rate limiting

## Trade-offs

**Pros:**

- Fixed memory usage
- O(1) all operations
- Cache-friendly sequential access
- No dynamic memory allocation

**Cons:**

- Fixed capacity limitation
- Potential for queue overflow
- Wasted space if not full
- More complex than simple queue

## Practice Problems

- **Design Circular Queue**: Implement with array
- **Task Scheduler**: Round-robin process scheduling
- **Moving Average**: Sliding window with circular buffer
- **Rate Limiter**: Token bucket with circular queue
- **Print Spooler**: Document queue management

<details>
<summary>Implementation Notes (Advanced)</summary>

### Index Management

- **Modulo arithmetic**: Efficient wraparound with % operator
- **Size tracking**: Separate size variable simplifies full/empty detection
- **Pointer advancement**: Both front and rear pointers move circularly
- **Boundary conditions**: Handle wrap-around edge cases

### Alternative Implementations

- **Two pointers**: front and rear with separate full flag
- **One empty slot**: Keep one slot empty to distinguish full/empty
- **Counter-based**: Use size counter (recommended approach)
- **Bit manipulation**: Power-of-2 sizes for faster modulo

### Memory Considerations

- **Cache locality**: Sequential access pattern is cache-friendly
- **Fixed allocation**: No memory fragmentation
- **Generic types**: Handle reference cleanup for garbage collection
- **Memory efficiency**: Better than linked list implementation

### Synchronization

- **Thread safety**: Requires synchronization for concurrent access
- **Lock-free**: Advanced implementations use atomic operations
- **Producer-consumer**: Built-in blocking capabilities
- **Wait/notify**: Coordinate between multiple threads

</details>
