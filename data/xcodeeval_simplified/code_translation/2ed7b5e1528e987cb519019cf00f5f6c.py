t1 = int(input())
t2 = int(input())
t3 = int(input())
t4 = int(input())
res = 0
if t1 == 0 and t3 == 0 and t4 == 0:
    res = 1
elif t1 == t4:
    if (t1 == 0 and t3 == 0) or t1 != 0:
        res = 1
print(res)