import math
log2 = lambda x: math.log(x) / math.log(2)
n, k = map(int, input().split())
m = 2 ** int(log2(n))
ans = m ^ (m - 1)
if k >= 2:
    print(n if ans > 2 * n else ans)
else:
    print(n)