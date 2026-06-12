l,r,a=input().split()
l=int(l)
r=int(r)
a=int(a)
if l<r and a>r-l:
    print(2*(l+(r-l)+(a-(r-l))//2))
elif l<r and a<=r-l:
    print(2*(l+(a)))
elif l>r and a>l-r:
    print(2*(r+(l-r)+(a-(l-r))//2))
elif l>r and a<=l-r:
    print(2*(r+(a)))
elif l==r:
    print(2*(r+(a//2)))
    
