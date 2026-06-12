memo = {}
n = int(input())
a = [s for s in input().split()]

def ok(c1, c2):
    return (c1[0] == c2[0]) or (c1[1] == c2[1])

def dfs(i, c1, c2, c3):
    k = (i, c1, c2, c3)
    if k in memo:
        return memo[k]
    if i < 0:
        memo[k] = ok(c1, c2) and ok(c1, c3)
    else:
        r = False
        if ok(c1, a[i]):
            r = r or dfs(i - 1, c2, c3, c1)
        if ok(c1, c2):
            r = r or dfs(i - 1, c1, c3, a[i])
        memo[k] = r
    return memo[k]

def check():
    if n == 1:
        return True;
    elif n == 2:
        return ok(a[1], a[0])
    else:
        return dfs(n - 4, a[-1], a[-2], a[-3])

print('YES' if check() else 'NO')




# Made By Mostafa_Khaled