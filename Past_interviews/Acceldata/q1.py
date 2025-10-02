def getMaxValue(currentValue, startTime, endtime, arr): # arr is a 4 x array
    for i in arr:
        eligibleRides = []
        print(i)
        if i[0] >= endtime:
            print("adding to eligible rides ", i)
            eligibleRides.append(i)
    print(f"debug {eligibleRides} {currentValue} {startTime} {endtime}")
    if len(eligibleRides) == 0:
        return currentValue
    else:
        maxVal = [];
        for ride in eligibleRides:
            maxVal.append(getMaxValue(currentValue + ride[3], ride[0], ride[1], arr))
        return maxVal
        



def getTripCost(arr):
    newArr = []
    for i in arr:
        a = [i[0], i[1], i[2], i[1]-i[0]+i[2]]
        newArr.append(a)
    return newArr

# arr = [[2,5,4],[1,5,1]]
# arr = getTripCost(arr)
# print (arr)
# print (getMaxValue(0, 0, 0, arr))
rides = [[1,6,1], 
                        [3,10,2], 
                        [10,12,3], 
                        [11,12,2], 
                        [12,15,2], 
                        [13,18,1]] 

rides = getTripCost(rides)
print(rides)
print (getMaxValue(0, 0, 0, rides))