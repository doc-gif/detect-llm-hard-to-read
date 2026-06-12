k,n,w=map(int,input().split())
s=((2*k+k*(w-1))*w)//2
if s>n:
    print(s-n)
else:
    print(0)