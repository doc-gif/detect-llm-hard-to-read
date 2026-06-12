n = int(input())

def rec(l):

    while l[-1] == l[-2]:
        l[-2] += 1
        l.pop()
    return l

res = [0]
for i in range(n):
    res.append(1)
    res = rec(res)

print(" ".join(map(str, res[1:])))