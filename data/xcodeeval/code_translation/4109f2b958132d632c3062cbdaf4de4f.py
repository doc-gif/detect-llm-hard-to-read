#codeforces 21b intersection, math

def readGen(transform):
	while (True):
		n=0
		tmp=input().split()
		m=len(tmp)
		while (n<m):
			yield(transform(tmp[n]))
			n+=1

readint=readGen(int)
A1,B1,C1=next(readint),next(readint),next(readint)
A2,B2,C2=next(readint),next(readint),next(readint)

def cross(a,b,c,d): return a*d-b*c

def zero(A1,B1): return A1**2 + B1**2 == 0

def lineIntersect(A1,B1,C1,A2,B2,C2):
	if (cross(A1,B1,A2,B2)==0):
		if (cross(A1,C1,A2,C2)==0 and cross(B1,C1,B2,C2)==0):
			# same line
			return -1
		else:
			# parallel
			return 0
	else:
		# cross
		return 1
	
def judge(A1,B1,C1,A2,B2,C2):
	if (zero(A1,B1) and C1!=0): return 0
	if (zero(A2,B2) and C2!=0): return 0
	
	if (not zero(A1,B1) and not zero(A2,B2)):
		# line and line
		return lineIntersect(A1,B1,C1,A2,B2,C2)
	else:
		return -1
	
print(judge(A1,B1,C1,A2,B2,C2))