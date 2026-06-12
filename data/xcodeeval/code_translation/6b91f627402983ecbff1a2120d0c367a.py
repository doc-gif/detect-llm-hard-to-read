def dis(x,y,d):
    if y==0 or x==d:
        return x+y
    else:
        return 4*d - x - y
d,x1,y1,x2,y2 = map(int, input().split())
a = abs(dis(x1,y1,d) - dis(x2,y2,d))
print(min(a, 4*d-a))