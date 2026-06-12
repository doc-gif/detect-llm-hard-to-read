# cook your dish here
import math
n = int(input())
cnt = 0
a = n
while a>0:
    x = a%10
    cnt = cnt + 1
    a = a//10
z = int(math.pow(10,cnt-1))
val = n%z
ans = n-val+int(math.pow(10,cnt-1))
print(ans - n)