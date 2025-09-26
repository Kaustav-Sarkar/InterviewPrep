***

# Algorithm & System Design Interview Notes

***

## 1. Search a 2D Sorted Matrix

**Problem:**  
Given an m x n matrix where each row and column is sorted in ascending order, determine if a target exists.

**Example:**
```
matrix = [
  [1,4,7,11,15],
  [2,5,8,12,19],
  [3,6,9,16,22],
  [10,13,14,17,24],
  [18,21,23,26,30]
]
target = 5
Output: true
```

**Approach:**
- Start from **top-right corner**.
- If current element == target → return true.
- If current element > target → move left.
- If current element < target → move down.

**Code:**
```java
public static boolean searchMatrix(int [][] matrix, int target){
    if (matrix == null || matrix.length == 0 || matrix[0].length == 0){
        return false;
    }
    int rows = matrix.length;
    int cols = matrix[0].length;
    int row = 0, col = cols - 1;
    while(row < rows && col >= 0){
        if(matrix[row][col] == target){
            return true;
        } else if (matrix[row][col] > target){
            col--;
        } else {
            row++;
        }
    }
    return false;
}
```

***

## 2. Shortest Path in a Binary Matrix

**Problem:**  
Given an n x n binary matrix `grid`, return the length of the shortest clear path from top-left to bottom-right, moving in 8 directions. Cells must be 0 to be traversable.

**Example:**
```
Input:
grid = [
  [0,0,0],
  [1,1,0],
  [1,1,0]
]
Output: 4
```

**Approach:**  
- Use **BFS** from (0,0), track (row, col, path_length) in the queue.
- For each cell, explore all 8 directions.
- Mark visited to avoid revisiting.
- If destination reached, return path length.

**Code:**
```java
public int shortestPathBinaryMatrix(int[][] grid){
    int n = grid.length;
    if(grid[0][0] != 0 || grid[n-1][n-1] != 0) return -1;

    int[][] directions = {
        {-1,-1},{-1,0},{-1,1},
        {0,-1},        {0,1},
        {1,-1}, {1,0}, {1,1}
    };
    Queue<int[]> queue = new LinkedList<>();
    queue.offer(new int[]{0,0,1});
    boolean[][] visited = new boolean[n][n];
    visited[0][0] = true;

    while(!queue.isEmpty()) {
        int [] current = queue.poll();
        int row = current[0], col = current[1], length = current[2];

        if(row == n-1 && col == n-1) return length;

        for (int[] dir : directions){
            int newRow = row + dir[0], newCol = col + dir[1];
            if(isValid(newRow, newCol, grid, visited)){
                visited[newRow][newCol] = true;
                queue.offer(new int[]{newRow, newCol, length+1});
            }
        }
    }
    return -1;
}

private boolean isValid(int r, int c, int[][] grid, boolean[][] visited){
    int n = grid.length;
    return r>=0 && c>=0 && r<n && c<n && grid[r][c]==0 && !visited[r][c];
}
```
- **Time Complexity:** $$O(n^2)$$  
- **Space Complexity:** $$O(n^2)$$

***

## 3. Maximum Subarray Sum (Kadane’s Algorithm)

**Problem:**  
Given an array, find the subarray with the maximum sum.

**Example:**
- Input: `{2, 3, -8, 7, -1, 2, 3}` ⟶ **Output:** 11 (`{7, -1, 2, 3}`)
- Input: `{-2, -4}` ⟶ **Output:** -2
- Input: `{5, 4, 1, 7, 8}` ⟶ **Output:** 25

**Code:**
```java
public int maxSubArraySum(int[] arr) {
    int maxSoFar = arr[0], currMax = arr[0];
    for (int i = 1; i < arr.length; i++) {
        currMax = Math.max(arr[i], currMax + arr[i]);
        maxSoFar = Math.max(maxSoFar, currMax);
    }
    return maxSoFar;
}
```

***

## 4. Low-Level Design: Distributed Task Queue

**Scenario:**  
Design a *distributed task queue* for a large-scale e-commerce platform to process async background jobs (emails, reports, orders, etc).

**Key Requirements:**
- **Priority Support:** Different task types and priorities.
- **Distributed Processing:** Workers across multiple machines.
- **Fault Tolerance:** Recover from worker failures (task re-queuing, acknowledgements, heartbeat).
- **Task Scheduling:** Immediate + delayed execution.
- **Monitoring & Retry:** Track status, retry failed tasks.
- **High Throughput:** Supports thousands of tasks per minute.

**Design Components:**
- **Task Producer:** Pushes tasks to the queue.
- **Central Broker/Queue (e.g., Redis, RabbitMQ, Kafka):** Stores & distributes tasks.
- **Workers:** Poll tasks, process jobs, send ack/nack.
- **Scheduler:** Schedules delayed tasks.
- **Failure Recovery:** Unacknowledged tasks re-queued.
- **Status Store:** Tracks progress, completion, retries.
- **Monitoring Dashboard:** Real-time status, alerts, metrics.

**Features to Consider:**
- **At-Least-Once Delivery:** Retry mechanism with deduplication.
- **Horizontal Scaling:** Add more workers for load.
- **Heartbeat Checks:** Remove/reassign dead workers’ tasks.
- **Dead Letter Queue:** Persistently failing tasks.

***

**Tip:** For interviews, briefly summarize approach (tradeoffs, bottlenecks, scaling, consistency vs availability) before writing detailed components. Draw a quick architecture diagram if allowed.

***