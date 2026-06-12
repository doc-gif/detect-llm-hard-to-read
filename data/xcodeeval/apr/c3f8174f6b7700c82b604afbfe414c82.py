import sys
input = lambda:sys.stdin.readline().rstrip()

T = int(input())

# keys = values of coin
# d = depth
# val = target value to make with coins
# cnt = number of coin left
def dfs(keys, d, val, cnt):
    if d == len(keys): return False
    key = keys[d]
    for c in range(cnt+1):
        if val - key*c < 0:
            return False
        elif val - key*c == 0 and cnt-c == 0:
            return True
        else:
            if d == len(keys):
                return False
            else:
                if dfs(keys, d+1, val - key*c, cnt-c): return True



for _ in range(T):
    n, m, k = map(int, input().split())
    if n%2 == 0 and m%2 == 0:
        if k%2 == 0:
            print('YES')
        else:
            print('NO')
    else:
        if m%2 == 0:
            n, m = m, n
        else:
            k = (n*m)//2 - k
        keys = [v for v in range(1, m+1, 2)]
        total = 0

        if dfs(keys, 0, k, n//2):
            print('YES')
        else:
            print('NO')
