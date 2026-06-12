import io
import os 
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
from types import GeneratorType 
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to 
    return wrappedfunc


from bisect import bisect_left 
def solve():
    n, m = map(int, input().split())
    a = []
    for i in range(m):
        ai, bi = map(int, input().split())
        a.append((ai, bi))
    a.sort(key = lambda x: x[0])
    b = []
    presum = [0]
    for i in range(m):
        b.append(a[i][1])
        a[i] = a[i][0]
        presum.append(presum[-1]+a[i])
    ma = 0
    for i in range(m):
        s = a[i]
        ind = bisect_left(a, b[i])
        if m-ind>n-1:
            s+=presum[m]-presum[m-n+1]
        else:
            s+=presum[m]-presum[ind]
            s+=b[i]*(n-1-(m-ind))
        if ind<=i:
            if m-ind<=n-1:
                s-=a[i]
                s+=b[i]
            else:
                s-=a[i]
                s+=a[m-n]
        #print(s)
        if s>ma:
            ma = s
    print(ma)
def main():
    t = int(input())
    for i in range(t):
        solve()
        if i!=t-1:
            input()
main()