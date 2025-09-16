# Multithreading in Java — Fundamentals, Patterns, and Examples

## Core Definitions

### Program

- **Definition**: Static collection of instructions and data stored on disk (executable/JAR/class files)
- **Characteristics**:
  - Passive entity: no execution context or resources
  - Many processes can be created from the same program

### Process

- **Definition**: Active instance of a program with allocated resources
- **Characteristics**:
  - Own virtual address space (heap, stacks, code, data)
  - Kernel tracks state via PCB (registers, file descriptors, etc.)
  - Inter-process communication (pipes, sockets, shared memory) requires kernel mediation

### Thread

- **Definition**: Lightweight execution unit within a process
- **Characteristics**:
  - Shares heap/code/descriptors with sibling threads
  - Own stack, registers, and program counter
  - Scheduled independently by OS/runtime
  - Easy communication via shared memory, but requires synchronization

### Multithreading

- **Definition**: Multiple threads executing concurrently within a process
- **Benefits**:
  - Parallelism on multi-core CPUs
  - Responsiveness (e.g., background work for UIs/servers)
  - I/O overlap (hide latency)
- **Challenges**:
  - Race conditions, visibility issues, and data corruption
  - Deadlocks and livelocks
  - Context-switch overhead, thread oversubscription

---

## Thread Lifecycle and Daemons

Java thread states: `NEW`, `RUNNABLE` (ready/running), `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`.

- **Daemon thread**: background thread that does not prevent JVM exit. Set via `setDaemon(true)` before `start()`. When only daemon threads remain, the JVM exits abruptly; do not rely on daemons for critical cleanup.
- **`join()`**: Current thread waits for another to terminate (optionally with timeout). Always handle `InterruptedException`.

```java
public class ThreadBasics {
    public static void main(String[] args) throws InterruptedException {
        Thread worker = new Thread(() -> {
            System.out.println("worker running: " + Thread.currentThread().getName());
            try { Thread.sleep(300); } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
            }
            System.out.println("worker done");
        }, "worker-1");

        worker.setDaemon(false); // set true for daemon behavior
        worker.start();

        // Wait for worker to finish
        worker.join();
        System.out.println("main done");
    }
}
```

---

## Sharing Data Safely: `synchronized`, `volatile`, Atomics

### The problem: race conditions

Concurrent updates to shared state (e.g., `count++`) are not atomic. Without synchronization you may observe lost updates and stale reads.

### Option 1 — `synchronized`

- Acquires the target object's intrinsic monitor. Intrinsic locks in Java are **reentrant**: the same thread can enter the same lock multiple times without self-deadlock.
- Establishes a happens-before relationship: unlock makes writes visible to subsequent lock acquisitions on the same monitor.

```java
class CounterSync {
    private int count = 0;

    public synchronized void increment() {
        count++; // atomic under the monitor
    }

    public synchronized int get() { return count; }
}
```

### Option 2 — `ReentrantLock`

- More control: `tryLock`, timed waits, fairness, multiple `Condition`s.
- Also reentrant. You must `unlock()` exactly as many times as you `lock()`; unlocking without ownership throws `IllegalMonitorStateException`.

```java
import java.util.concurrent.locks.*;

class CounterLock {
    private final ReentrantLock lock = new ReentrantLock();
    private int count = 0;

    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }

    public int get() {
        lock.lock();
        try { return count; }
        finally { lock.unlock(); }
    }
}
```

Timed acquisition to reduce deadlock risk:

```java
boolean acquired = lock.tryLock(200, java.util.concurrent.TimeUnit.MILLISECONDS);
if (acquired) {
    try { /* work */ }
    finally { lock.unlock(); }
} else {
    // fallback or retry
}
```

### Option 3 — Atomics

- Lock-free, memory-safe primitives for simple cases.

```java
import java.util.concurrent.atomic.AtomicInteger;

class CounterAtomic {
    private final AtomicInteger count = new AtomicInteger();
    public void increment() { count.incrementAndGet(); }
    public int get() { return count.get(); }
}
```

### Visibility-only flags — `volatile`

Use for flags where compound operations are not required.

```java
class StoppableWorker implements Runnable {
    private volatile boolean running = true; // guarantees visibility

    public void stop() { running = false; }

    @Override public void run() {
        while (running) {
            // do work
            if (Thread.currentThread().isInterrupted()) break;
        }
    }
}
```

---

## Low-level Coordination: `wait/notify`

`wait()` releases the monitor and suspends the thread until `notify()`/`notifyAll()` on the same monitor. Always call `wait()` in a loop and hold the monitor when calling `wait/notify`.

```java
import java.util.*;

class BoundedBuffer<T> {
    private final Queue<T> q = new ArrayDeque<>();
    private final int capacity;

    BoundedBuffer(int capacity) { this.capacity = capacity; }

    public synchronized void put(T item) throws InterruptedException {
        while (q.size() == capacity) wait();
        q.add(item);
        notifyAll();
    }

    public synchronized T take() throws InterruptedException {
        while (q.isEmpty()) wait();
        T t = q.remove();
        notifyAll();
        return t;
    }
}
```

Prefer higher-level utilities from `java.util.concurrent` when possible.

---

## High-level Coordination Utilities

### `CountDownLatch` — wait for N things to complete

```java
import java.util.concurrent.*;

class LatchDemo {
    public static void main(String[] args) throws InterruptedException {
        int workers = 3;
        CountDownLatch ready = new CountDownLatch(workers);

        ExecutorService pool = Executors.newFixedThreadPool(workers);
        for (int i = 0; i < workers; i++) {
            pool.execute(() -> {
                // initialize
                ready.countDown();
            });
        }

        ready.await();
        System.out.println("All workers initialized");
        pool.shutdown();
    }
}
```

### `Semaphore` — limit concurrency

```java
import java.util.concurrent.Semaphore;

class SemaphoreDemo {
    private final Semaphore permits = new Semaphore(5);

    public void handleRequest() throws InterruptedException {
        permits.acquire();
        try { /* process */ }
        finally { permits.release(); }
    }
}
```

### `CyclicBarrier` — wait for all parties then proceed (reusable)

Use when a fixed number of threads must rendezvous at a barrier, optionally with a barrier action.

---

## Executors and Thread Pools

Prefer pools over manually creating threads for server-style workloads.

```java
import java.util.List;
import java.util.concurrent.*;

class ExecutorExamples {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService pool = Executors.newFixedThreadPool(4);

        Future<Integer> f = pool.submit(() -> 1 + 1);
        System.out.println("result: " + f.get());

        List<Callable<Integer>> tasks = List.of(
            () -> 10, () -> 20, () -> 30
        );
        for (Future<Integer> r : pool.invokeAll(tasks)) {
            System.out.println(r.get());
        }

        pool.shutdown();
        if (!pool.awaitTermination(5, TimeUnit.SECONDS)) {
            pool.shutdownNow();
        }
    }
}
```

For production, configure `ThreadPoolExecutor` directly (queue size, rejection policy, thread factory, naming, etc.).

---

## Avoiding Deadlocks

Deadlock requires: mutual exclusion, hold-and-wait, no preemption, and circular wait. Break the cycle:

- Impose a global lock ordering and acquire locks in that order
- Use `tryLock` with timeouts and backoff
- Minimize lock scope and shared mutable state

```java
import java.util.concurrent.locks.ReentrantLock;

class OrderedLocks {
    private final ReentrantLock lockA = new ReentrantLock();
    private final ReentrantLock lockB = new ReentrantLock();

    public void doWorkOrdered() {
        ReentrantLock first = lockA, second = lockB; // fixed order
        first.lock();
        try {
            second.lock();
            try { /* work with A then B */ }
            finally { second.unlock(); }
        } finally { first.unlock(); }
    }
}
```

Note: Reentrancy prevents a thread from deadlocking on the same lock it already owns, but does not prevent multi-lock deadlocks across different threads.

---

## Java Memory Model (JMM) Essentials

- Writes by one thread become visible to another only through a happens-before edge: lock/unlock of the same monitor, `volatile` write→read, thread start/join, and certain `java.util.concurrent` operations.
- `volatile` provides visibility and ordering (no reordering around volatile) but not atomicity of compound actions.
- Do not publish mutable objects without proper synchronization or safe publication patterns.

---

## Best Practices Checklist

- Prefer immutability and confinement of state to a single thread
- Use high-level concurrency utilities before low-level `wait/notify`
- Name your threads; handle `InterruptedException` by restoring interrupt status
- Avoid blocking in synchronized blocks; keep critical sections small
- Use timeouts for blocking operations where possible
- Avoid `Thread.stop/suspend/resume` (deprecated/dangerous)
- For caches/collections, use `ConcurrentHashMap`, `CopyOnWriteArrayList`, etc.

---

## Quick Recap / Q&A

- Daemon vs user threads: daemon threads do not keep the JVM alive; user threads do.
- Waiting for a thread: call `t.join()` (optionally with timeout) and handle interruptions.
- Safe increment of a shared counter: `synchronized`, `ReentrantLock`, or `AtomicInteger`.
- Avoiding deadlocks: lock ordering or timed `tryLock` with fallback.
