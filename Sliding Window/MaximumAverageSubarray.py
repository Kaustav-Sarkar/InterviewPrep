class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        maxsum = sum(nums[0:k])
        s = maxsum
        for i in range(len(nums)-k):
            s = s - nums[i] + nums[i+k]
            maxsum = max(s, maxsum) 
        return round(maxsum/k,5)