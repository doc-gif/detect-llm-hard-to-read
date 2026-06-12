import sys

def minp():
	return sys.stdin.readline().strip()

def mint():
	return int(minp())

def mints():
	return map(int,minp().split())

n,m,mi,ma = mints()
a = list(mints())
mii = min(a)
maa = max(a)
if mii > mi:
	m += 1
if maa < ma:
	m += 1
if mii < mi or maa > ma or m > n:
	print("Incorrect")
else:
	print("Correct")
