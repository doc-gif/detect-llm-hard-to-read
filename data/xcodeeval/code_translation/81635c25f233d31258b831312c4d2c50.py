import sys
from math import *

def minp():
	return sys.stdin.readline().strip()

def mint():
	return int(minp())

def mints():
	return map(int, minp().split())

n = mint()
p = [0]*n
x = dict()
y = dict()
for i in range(n):
	a = tuple(mints())
	p[i] = a
	if a[0] in x:
		x[a[0]].append(i)
	else:
		x[a[0]] = [i]
	if a[1] in y:
		y[a[1]].append(i)
	else:
		y[a[1]] = [i]

del(pow)
r = 1
q = [0]*n
w = [True]*n
ql = 0
qr = 0
for i in range(n):
	if w[i]:
		w[i] = False
		q[qr] = i
		qr += 1
		qlb = ql
		e = 0
		xs = set()
		ys = set()
		while ql < qr:
			v = q[ql]
			ql += 1
			a = p[v]
			if a[0] not in xs:
				xs.add(a[0])
				e -= 1
				for u in x[a[0]]:
					e += 1
					if w[u]:
						w[u] = False
						q[qr] = u
						qr += 1
			if a[1] not in ys:
				ys.add(a[1])
				e -= 1
				for u in y[a[1]]:
					e += 1
					if w[u]:
						w[u] = False
						q[qr] = u
						qr += 1
		vc = ql-qlb
		#print(vc,e,vc-1)
		if vc-1 == e:
			r = (r*(pow(2,vc+1,1000000007)-1))%1000000007
		else:
			r = (r*(pow(2,len(xs)+len(ys),1000000007)))%1000000007
print(r)