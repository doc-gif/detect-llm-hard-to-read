n, m = map(int, input().split())

if n == 2:
	print(0)
	exit()

mod = 998244353 
ans = ((n-2) * pow(2, n-3, mod)) % mod
# print(ans)
for i in range(m-n+2, m+1):
	ans = (ans * i) % mod
# print(ans)
fact = 1
for i in range(2, n):
	fact = (fact*i) % mod

fact = pow(fact, mod-2, mod)
ans = (ans * fact) % mod

print(ans)