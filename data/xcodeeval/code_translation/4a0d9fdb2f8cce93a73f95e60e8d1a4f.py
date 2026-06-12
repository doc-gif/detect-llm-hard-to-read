def check(h,m):
    if('7' in str(h) or '7' in str(m)):
        return True
    return False


x=int(input())
h,m=map(int,input().split())
c=0
while True:
    if not check(h,m):
        m-=x
        c+=1
        if m<0:
            m=(m+60)%60
            h-=1
        if h<0:
            h=23
            m=(m+60)%60
    else:
        break
print(c)
