I=lambda:map(int,input().split())

R=range

n,m,k=I()

def r(a,b,c=k):

	q=0

	for a,b in sorted((b[i][1]-a[i][0],a[i][2])for i in R(m))[::-1]:

		if a<1or c<1:break

		q+=a*min(b,c);c-=b

	return q

w=[]

for _ in '0'*n:I();w+=[[list(I())for _ in '0'*m]]

print(max(r(w[i],w[j])for i in R(n)for j in R(n)))




# Made By Mostafa_Khaled