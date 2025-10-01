"""
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

    The left 

    of a node contains only nodes with keys strictly less than the node's key.
    The right subtree of a node contains only nodes with keys strictly greater than the node's key.
    Both the left and right subtrees must also be binary search trees.

 

Example 1:

Input: root = [2,1,3]
Output: true

Example 2:

Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.

 

Constraints:

    The number of nodes in the tree is in the range [1, 104].
    -231 <= Node.val <= 231 - 1

"""

from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Simple inorder and checking array
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        arr = []
        def inOrder(node):
            if not node:
                return
            inOrder(node.left)
            arr.append(node.val)
            inOrder(node.right)
        inOrder(root)
        if len(arr) < 2:
            return True
        for i in range(1,len(arr)):
            if arr[i] <= arr[i-1]:
                return False
        return True


# Solution using recursion, sets the leftmost val to -inf and rightMost val to +inf the keeps comparing if the node is ever in the wrong range
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node, min_val, max_val):
            if not node:
                return True
            if node.val <= min_val or node.val >= max_val:
                return False
            return (validate(node.left, min_val, node.val) and 
                    validate(node.right, node.val, max_val))
        
        return validate(root, float('-inf'), float('inf')) 