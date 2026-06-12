
def playingCubes(n,m):
	print((m+n-1) - min(m,n) ,min(m,n))

n,m = input().split()
playingCubes(int(n),int(m))