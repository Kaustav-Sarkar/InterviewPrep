"""
Given an m x n matrix, return all elements of the matrix in spiral order.

 

Example 1:

Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

Example 2:

Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]

 

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 10
    -100 <= matrix[i][j] <= 100

 
"""

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        left = 0
        right = len(matrix[0]) -1
        top = 0
        bottom = len(matrix) -1
        result = []
        i = 0
        total = (right+1) * (bottom+1)
        while i < total:
            print(left, right, top, bottom)
            pointer = left
            if left > right or top > bottom:
                break
            while(pointer <=  right):
                result.append(matrix[top][pointer])
                pointer+=1
                i+=1
            top+=1
            pointer = top
            if left > right or top > bottom:
                break
            while(pointer <= bottom):
                result.append(matrix[pointer][right])
                pointer+=1
                i+=1
            right-=1
            pointer = right
            if left > right or top > bottom:
                break
            while(pointer>=left):
                result.append(matrix[bottom][pointer])
                pointer-=1
                i+=1
            bottom-=1
            pointer = bottom
            if left > right or top > bottom:
                break
            while (pointer >= top):
                result.append(matrix[pointer][left])
                pointer-=1
                i+=1
            left+=1
        return result