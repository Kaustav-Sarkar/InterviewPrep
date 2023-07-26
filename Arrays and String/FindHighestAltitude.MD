# Highest Altitude Problem

This repository contains a Python solution for the problem of finding the highest altitude a biker can reach on a road trip.

## Problem Statement

A biker is going on a road trip. The road trip consists of `n + 1` points at different altitudes. The biker starts his trip on point 0 with altitude equal 0.

You are given an integer array `gain` of length `n` where `gain[i]` is the net gain in altitude between points `i` and `i + 1` for all `(0 <= i < n)`. The task is to return the highest altitude of a point.

### Examples

**Example 1:**

```python
Input: gain = [-5,1,5,0,-7]
Output: 1
Explanation: The altitudes are [0,-5,-4,1,1,-6]. The highest is 1.

Input: gain = [-4,-3,-2,-1,4,3,2]
Output: 0
Explanation: The altitudes are [0,-4,-7,-9,-10,-6,-3,-1]. The highest is 0.
```

# Solution Summary

The solution to this problem is based on a single pass through the `gain` array while maintaining the current altitude and the maximum altitude seen so far.

At the start, both the current altitude (`curr_alt`) and the maximum altitude (`max_alt`) are initialized to 0. Then, for each gain in altitude `i` in the `gain` array, the `curr_alt` is updated by adding `i` to it, and `max_alt` is updated if `curr_alt` is higher than the current `max_alt`.

Finally, after iterating through all the elements in the `gain` array, the solution returns `max_alt`, which holds the maximum altitude the biker has reached.

This approach leverages the concept of a single pass and dynamic updating of variables, making it efficient with a time complexity of O(n), where n is the length of the `gain` array.
