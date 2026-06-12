import sys
input = sys.stdin.buffer.readline
def print(val):
    sys.stdout.write(str(val) + '\n')

def choose(n,k,mod = None):
    if k > n:
        return 0
    k = min(n-k,k)
    total = 1
    for i in range(n-k+1, n+1):
        total*= i 
    for i in range(2,k+1):
        total//= i
    return total % 998244353
def factorial(n):
    total = 1
    for i in range(2, n+1):
        total*= i
        total %=998244353
    return total
def place_rooks(n,k):
    if k == 0:
        return factorial(n)
    filled = n - k
    placements_per_filled = 0
    for i in range(filled):
        mult = 1
        for _ in range(n):
            mult *= (filled-i)
            mult %= 998244353
        placements_per_filled += ((-1)**i)*choose(filled,i)*mult
        placements_per_filled %= 998244353
    total = (2*choose(n,filled)*placements_per_filled ) % 998244353
    if k == 0:
        total//= 2
    return total
        
n, k = map(int,input().split())
print(place_rooks(n,k))
