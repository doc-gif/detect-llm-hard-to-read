import math
s = input()
n = int(s.split()[0])
k = int(s.split()[1])
st = input()
i = 1
arr = list(map(int, st.split()))
j = (sum(arr) + k * i)/(len(arr) + i)
if(j-math.trunc(j)>=0.5):
    j = math.ceil(j)
else:
    j = math.trunc(j)
if(j == k):
    print(0)
else:
    while(True):
        j = (sum(arr) + k * i)/(len(arr) + i)
        if(j-math.trunc(j)>=0.5):
            j = math.ceil(j)
        else:
            j = math.trunc(j)
        if(j == k):
            print(i)
            break
        i += 1
