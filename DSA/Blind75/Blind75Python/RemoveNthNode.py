"""
Given the head of a linked list, remove the nth node from the end of the list and return its head.

 

Example 1:

Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]

Example 2:

Input: head = [1], n = 1
Output: []

Example 3:

Input: head = [1,2], n = 1
Output: [1]

 

Constraints:

    The number of nodes in the list is sz.
    1 <= sz <= 30
    0 <= Node.val <= 100
    1 <= n <= sz

 

Follow up: Could you do this in one pass?
"""
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        if head.next == None and n == 1:
                    return None
        firstPointer = head
        secondPointer = head
        i = 0
        
        while i <= n and secondPointer is not None:
            print(secondPointer.val)
            secondPointer = secondPointer.next
            i+=1

        while(i<=n):
            firstPointer = firstPointer.next
            return firstPointer

        while(secondPointer):
            firstPointer = firstPointer.next
            secondPointer = secondPointer.next

        firstPointer.next = firstPointer.next.next
        return head