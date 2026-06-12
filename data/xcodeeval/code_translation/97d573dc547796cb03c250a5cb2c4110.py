from math import*
n=int(input())

i=1
while i*(i+1)<2*n+2:
    if(i*(i+1)==2*n):
        print("YES")
        exit()
    i+=1

print("NO")

