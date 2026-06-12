a,b=map(int,input().split())
def bn(x):
        m=0
        while x>0:
                m+=x%2
                x//=2
        return m

mn=100000000
idx=0
if b==0:
        print(bn(a))
        exit(0)
else:
        for n in range(1,100):
                j=n*b
                if a<=j:
                        break
                elif bn(a-j)<=n and a-j>=n:
                        print(n)
                        exit(0)
print(-1)