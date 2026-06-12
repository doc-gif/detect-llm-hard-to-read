strno=input()
n=len(strno)
sum1=0
for i in range(1,n):
    sum1 += 1<<i
for i in range(n):
    if strno[i]=='7':
        sum1 += 1<<(n-i-1)
print(sum1+1)
