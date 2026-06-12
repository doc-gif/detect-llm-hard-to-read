n = int(input())
ans = 1
mod = 10**9+7
temp = 0.5
for i in range(n):
    ans = (ans*(i+1))%mod
    temp = (temp*2)%mod
print((ans-int(temp))%mod)
