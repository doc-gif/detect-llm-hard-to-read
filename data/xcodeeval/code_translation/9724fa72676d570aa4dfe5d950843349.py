import bisect
def LIS(As):
    L = [As[0]]
    for a in As[1:]:
        if a >= L[-1]:
            L.append(a)
        else:
            pos = bisect.bisect_right(L, a)
            L[pos] = a
    return L

def solve():
    n,T = map(int,input().split())
    array = list(map(int,input().split()))
    if (T<=n+1):
        print (len(LIS(array*T)))
    else:
        newarray = array*n
        lis = LIS(newarray)
        newlis = LIS(newarray+array)
        print (len(newlis)+(len(newlis)-len(lis))*(T-n-1))

solve()