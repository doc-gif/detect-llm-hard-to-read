k, a, b = list(map(lambda x: int(x), input().split()))
r = 0
aa = b // k
bb = a // k
a %= k
b %= k
r += aa + bb
aa *= k-1
bb *= k-1
if not (a <= aa and b <= bb):
    print(-1)
else:
    print(r)