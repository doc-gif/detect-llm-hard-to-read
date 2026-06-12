n, k = [int(x) for x in input().split()]
     
summ=0
for i in range(1,n+1):
    summ+=i
    candy = summ - (n-i)
    if candy == k:
        index=i
        break 
print(n-index)