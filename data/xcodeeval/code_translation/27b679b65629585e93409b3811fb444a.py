import sys
from math import factorial

input = sys.stdin.readline

def A(n, k):
	return factorial(n)//factorial(n-k)

def solve():
	n, mod = map(int, input().split())
	if n == 1:
		print(0)
		return
	z = [1]
	aaa = 0
	for i in range(2,n+1):
		nz = [0]*((i-1)*i//2+1)
		d = [0]*(len(z)+1)
		for w in range(len(z)-1, -1, -1):
			d[w] = (d[w+1] + z[w]) % mod
		for w in range(len(nz)):
			#d = 0
			#for j in range(max(0,w+1-i), min(len(z),w+1)):
			#	d = (d + z[j]) % mod
			#nz[w] = d
			L = max(0,w+1-i)
			R = min(len(z)-1,w)
			nz[w] = d[L]-d[R+1]
		e = [0]*(len(d)+1)
		f = [0]*(len(d)+1)
		for w in range(0, len(e)-1):
			e[w+1] = (e[w] + d[w]) % mod
			f[w+1] = (f[w] - w * d[w]) % mod
		R = len(z)
		bbb = 0
		for jj in range(max(0,len(z)-i), len(z)-2):
			L = jj + 2
			bbb = (bbb + ((e[R] - e[L]) * (i+1+jj) \
				+ (f[R] - f[L])) * z[jj]) % mod
		for jj in range(len(z)-i):
			L = jj + 2
			R = i + jj
			bbb = (bbb + ((e[R+1] - e[L]) * (i+1+jj) \
				+ (f[R+1] - f[L])) * z[jj]) % mod
		#print(bbb)
		aaa += (bbb * A(n,n-i)) % mod
		#print(nz)
		z = nz
	#print(z)
	print(aaa % mod)

solve()
