# Multithreading Fundamentals

## Core Definitions

### Program

- **Definition**: Static collection of instructions and data stored on disk (executable file)
- **Characteristics**:
  - Passive entity containing machine code, libraries, and metadata
  - No execution context or system resources allocated
  - Multiple processes can run from the same program binary
  - Compiled/interpreted code ready for execution by OS loader

### Process

- **Definition**: Active instance of a program loaded into memory with allocated system resources
- **Characteristics**:
  - Has its own virtual address space (heap, stack, code segment, data segment)
  - OS-managed process control block (PCB) tracks state, registers, file descriptors
  - Inter-process communication requires kernel mediation (pipes, sockets, shared memory)
  - Process creation involves expensive system calls (fork/exec) and memory allocation
  - Complete isolation provides fault tolerance but limits sharing

### Thread

- **Definition**: Lightweight execution unit within a process sharing address space
- **Characteristics**:
  - Shares heap, code segment, data segment, and file descriptors with sibling threads
  - Maintains private stack, registers, and program counter
  - OS scheduler treats threads as independent execution entities
  - Thread creation bypasses memory allocation overhead
  - Direct memory sharing enables efficient communication but requires synchronization

### Multithreading

- **Definition**: Concurrent execution of multiple threads within a single process
- **Benefits**:
  - Parallelism: True parallel execution on multi-core systems
  - Responsiveness: Non-blocking UI through background thread processing
  - Resource efficiency: Shared memory reduces overhead vs. multi-process
  - I/O optimization: Overlapping computation with blocking operations
- **Challenges**:
  - Race conditions and data corruption without proper synchronization
  - Deadlocks from circular lock dependencies
  - Context switching overhead at high thread counts

## Thread Lifecycle States

 Deamon threads are background threads, you can set this using `myThread.setDeamon(true)` and if the main thread ends, this will be killed too
 A regular thread won't be killed even if the main is killed
 To make the main thread wait for the other threads you have to do t1.join(), otherwise the main thead can end anytime

If a single object is used between threads, use the synchronized keyword to ensure only 1 thread can access a method at a time, eg `public synchronized void increment () {}`

ReentrantLock is smart enough to understand when the lock is held by the same thread requesting the lock so a deadlock is not possible Thread1(aquires lock)-> Thread1 (requests lock) won't cause a deadlock. It also maintains a counter for the number of unlocks and locks, so if they don't match, the lock stays locked, exceptions are raised if the number of locks and unlocks don't match.
