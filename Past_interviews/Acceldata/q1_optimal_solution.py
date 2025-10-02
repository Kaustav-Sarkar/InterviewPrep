def maxTaxiEarnings(n, rides):
    """
    Optimal solution using Dynamic Programming + Binary Search
    Time Complexity: O(m log m) where m is number of rides
    Space Complexity: O(m)
    """
    # Step 1: Calculate profit for each ride and sort by end time
    rides_with_profit = []
    for start, end, tip in rides:
        profit = end - start + tip
        rides_with_profit.append((start, end, profit))
    
    # Sort by end time - this is crucial for DP approach
    rides_with_profit.sort(key=lambda x: x[1])
    
    m = len(rides_with_profit)
    if m == 0:
        return 0
    
    # Step 2: DP array where dp[i] = max profit from rides 0 to i
    dp = [0] * m
    dp[0] = rides_with_profit[0][2]  # First ride profit
    
    # Step 3: For each ride, decide to take it or not
    for i in range(1, m):
        current_start, current_end, current_profit = rides_with_profit[i]
        
        # Option 1: Don't take current ride
        profit_without_current = dp[i-1]
        
        # Option 2: Take current ride
        # Find latest ride that doesn't conflict (ends before current starts)
        latest_non_conflicting = findLatestNonConflicting(rides_with_profit, i)
        
        profit_with_current = current_profit
        if latest_non_conflicting != -1:
            profit_with_current += dp[latest_non_conflicting]
        
        # Take maximum of both options
        dp[i] = max(profit_without_current, profit_with_current)
    
    return dp[m-1]

def findLatestNonConflicting(rides, current_index):
    """
    Binary search to find the latest ride that ends before current ride starts
    This is the key optimization that makes this O(n log n) instead of O(n²)
    """
    current_start = rides[current_index][0]
    
    left, right = 0, current_index - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if rides[mid][1] <= current_start:  # End time <= start time of current
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Test with the examples
def test_solution():
    # Example 1
    n1 = 5
    rides1 = [[2,5,4], [1,5,1]]
    result1 = maxTaxiEarnings(n1, rides1)
    print(f"Example 1: Expected 7, Got {result1}")
    
    # Example 2
    n2 = 20
    rides2 = [[1,6,1], [3,10,2], [10,12,3], [11,12,2], [12,15,2], [13,18,1]]
    result2 = maxTaxiEarnings(n2, rides2)
    print(f"Example 2: Expected 20, Got {result2}")
    
    # Let's trace through example 2 to understand
    print("\n--- Tracing Example 2 ---")
    traceExample2()

def traceExample2():
    """Trace through example 2 to show the decision process"""
    rides = [[1,6,1], [3,10,2], [10,12,3], [11,12,2], [12,15,2], [13,18,1]]
    
    # Calculate profits
    rides_with_profit = []
    for start, end, tip in rides:
        profit = end - start + tip
        rides_with_profit.append((start, end, profit))
        print(f"Ride [{start},{end},{tip}] -> Profit: {end}-{start}+{tip} = {profit}")
    
    # Sort by end time
    rides_with_profit.sort(key=lambda x: x[1])
    print(f"\nAfter sorting by end time: {rides_with_profit}")
    
    # The optimal selection would be:
    # Take ride [1,6,1] with profit 6, then [10,12,3] with profit 5, then [12,15,2] with profit 5, then [13,18,1] with profit 6
    # But actually, let's see what the algorithm chooses:
    
    print(f"\nOptimal solution gives: {maxTaxiEarnings(20, rides)}")

if __name__ == "__main__":
    test_solution()

