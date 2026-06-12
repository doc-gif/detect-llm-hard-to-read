n, k, x = map(int, input().split())
a = sorted(list(map(int, input().split())))
result=k*x
for i in range(n-k):
	result+=a[i]
print(result)