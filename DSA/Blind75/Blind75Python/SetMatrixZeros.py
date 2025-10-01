"""
Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.

 

Example 1:

Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]

Example 2:

Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

 

Constraints:

    m == matrix.length
    n == matrix[0].length
    1 <= m, n <= 200
    -231 <= matrix[i][j] <= 231 - 1

 

Follow up:

    A straightforward solution using O(mn) space is probably a bad idea.
    A simple improvement uses O(m + n) space, but still not the best solution.
    Could you devise a constant space solution?


"""
from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        firstRow = None
        firstColumn = None

        cols = len(matrix[0])
        rows = len(matrix)
        for i in range(cols):
            if matrix[0][i] == 0:
                firstRow = 0
        for i in range(rows):
            if matrix[i][0] == 0:
                firstColumn = 0
        for i in range(1,rows):
            for j in range(1,cols):
                if matrix[i][j]==0:
                    matrix[i][0]=0
                    matrix[0][j]=0
        for i in range(1,cols):
            if matrix[0][i] == 0:
                for j in range(rows):
                    matrix[j][i] = 0
        for i in range(1,rows):
            if matrix[i][0] == 0:
                for j in range(cols):
                    matrix[i][j] = 0
        
        if firstRow == 0:
            for i in range(cols):
                matrix[0][i]=0
        if firstColumn ==0:
            for i in range(rows):
                matrix[i][0] = 0
        return matrix