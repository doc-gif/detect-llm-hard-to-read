n, e = map(int, input().split())
groups = 0
small = min(n, e)
big = max(n, e)
for i in range(big):
    if big >= 2 and small >= 1:
        groups += 1
        big -= 2
        small -= 1
    elif big >= 1 and small >= 2:
        groups += 1
        big -= 1
        small -= 2
    else:
        break
    #print(small, big)
    a = small
    b = big
    small = min(a, b)
    big = max(a, b)
    #print(small, big)
    #print("\n")
print(groups)
