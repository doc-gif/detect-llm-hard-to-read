import sys
from math import factorial

input = sys.stdin.readline

total = 0
dd = dict()
qwe = set()

def stup(a, was, i, n, ans):
	if i == n:
		zz = 0
		for i in range(n):
			for j in range(i):
				if a[j] > a[i]:
					zz += 1
		print(a, zz)
		ans[zz] += 1
		return
	for v in range(n):
		if not was[v]:
			was[v] = True
			a[i] = v
			stup(a, was, i+1, n, ans)
			was[v] = False

zz, mod = map(int, input().split())
if zz == 1:
	print(0)
	exit(0)
#ans = [0]*(zz*(zz-1))
#stup([0]*zz, [False]*zz, 0, zz, ans)
#print(ans)

def C(n, k):
	return factorial(n)//factorial(n-k)//factorial(k)

z = [1]
aaa = mod-1
for i in range(2,zz):
	nz = [0]*(i*i//2)
	for j in range(len(z)):
		for k in range(i):
			if z[j] > 0:
				#print(i-k+j, j, i-k-1)
				nz[i-k-1+j] += z[j]
	for k in range(zz):
		for l in range(i+1,zz):
			for j in range(len(z)):
				for jj in range(len(z)):
					if i-k-1+j > i-l-1+jj:
						aaa = (aaa + z[j] * z[jj] * C(zz,i)) % mod
	#print(nz)
	z = nz
#print(z)
print(aaa % mod)
exit(0)
def solve():
	pass

solve()
