y,b,r=map(int,input().split())
m=min(y,b,r)
if y==b and y==r:
    print(3*b-3)
else:
    if m==y and y!=b and y!=r:
        if r<y+2:
            print(3*y)
        else:
            print(3*y+3)
    elif m==b and b!=r:
        print(3*b)
    elif m==r:
        print(3*r-3)