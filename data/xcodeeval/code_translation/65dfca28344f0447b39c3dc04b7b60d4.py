def getMax(num):
    arr = list(num)
    prod = 1
    for a in arr:
        prod = prod*int(a)
    return prod

n = input()
num = list(n)

i = len(n)-1
maxP = getMax(n)

if len(n) > 1:
    while i>0:
        num[i] = '9'
        while int(num[i-1]) == 0:
            num[i-1] = '9'
            i = i - 1
        if int(num[i-1]) > 1:
            num[i-1] = str(int(num[i-1]) - 1)

        #print(num)
        maxP = max(getMax(''.join(num)),maxP)
        i = i-1
    print(maxP)
else:
    print(n)
"""




minNum = num[:]
minNum[0]  = int(minNum[0]) - 1
minNum[0] = str(minNum[0])
for i in range(1,len(minNum)):
    minNum[i] = '9'

minN = ''.join(minNum)
minN = int(minN)
n = int(n)

maxP = 0
for a in range(minN,n+1):
    maxP = max(getMax(str(a)),maxP)
print(maxP)

"""