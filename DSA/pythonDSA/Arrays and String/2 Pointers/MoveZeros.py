class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        l = len(nums)
        i = 0
        nonzero = 0
        zero = 0
        while(i<l):
            if nums[i]==0:
                zero+=1
            else:
                nums[nonzero]=nums[i]
                nonzero+=1
            i+=1
        for i in range(l-zero, l):
            nums[i] = 0
