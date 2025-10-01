"""
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

 

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:

Input: root = [1]
Output: [[1]]

Example 3:

Input: root = []
Output: []

 

Constraints:

    The number of nodes in the tree is in the range [0, 2000].
    -1000 <= Node.val <= 1000


"""
from collections import deque
from typing import Optional, List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# In BFS always run a forloop when inside the while loop to get all the elements

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        bfsQueue = deque()
        finalArray = []
        if not root:
            return finalArray
        bfsQueue.append(root)
        while bfsQueue:
            newArray = []
            l = len(bfsQueue)
            for i in range(l):
                element = bfsQueue.popleft()
                if element:
                    newArray.append(element.val)
                    bfsQueue.append(element.left)
                    bfsQueue.append(element.right)
            if len(newArray)>0:
                finalArray.append(newArray)
        return finalArray


