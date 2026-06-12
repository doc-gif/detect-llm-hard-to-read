n, e = map(int, input().split())
groups = 0
small = min(n, e)
big = max(n, e)
for _ in range(big):
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
    small, big = min(small, big), max(small, big)
print(groups)