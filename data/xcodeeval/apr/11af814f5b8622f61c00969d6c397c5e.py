import sys
input=sys.stdin.readline
mod = 998244353
sys.setrecursionlimit(pow(10, 8))

def power(x, y):
    if   y == 0: return 1
    elif y == 1	 : return x % mod
    elif y % 2 == 0 : return power(x, y//2)**2 % mod
    else: return power(x, (y-1)//2)**2 * x % mod
    

def modinv(a):
    b, u, v = mod, 1, 0
    while b:
        t = a//b
        a, u = a-t*b, u-t*v
        a, b, u, v = b, a, v, u
    u %= mod
    return u

def cmb(n, r):
    if ( r<0 or r>n ):
        return 0
    r = min(r, n-r)
    return g1[n] * g2[r] * g2[n-r] % mod

NNN = 2*10**5
g1 = [1, 1]
g2 = [1, 1]
inverse = [0, 1]

for i in range( 2, NNN + 1 ):
    g1.append( ( g1[-1] * i ) % mod )
    inverse.append( ( -inverse[mod % i] * (mod//i) ) % mod )
    g2.append( (g2[-1] * inverse[-1]) % mod )

N, K = map(int, input().split())
if K > N:
    print(0)
else:
    M=N-K
    R = 0
    for i in range(1, M+1):
        R += (-1 if (M-i)%2 else 1) * cmb(M, i) * power(i, N) % mod
    R = R*cmb(N, M)%mod
    if K != 0:
        R = R*2%mod
    print(R)
