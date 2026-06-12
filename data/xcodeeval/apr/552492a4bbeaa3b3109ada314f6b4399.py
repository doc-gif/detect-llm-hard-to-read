#import time

def make_nCr_mod(max_n=2 * 10**5, mod=10**9 + 7):
    max_n = min(max_n, mod - 1)

    fact, inv_fact = [0] * (max_n + 1), [0] * (max_n + 1)
    fact[0] = 1
    for i in range(max_n):
        fact[i + 1] = fact[i] * (i + 1) % mod

    inv_fact[-1] = pow(fact[-1], mod - 2, mod)
    for i in reversed(range(max_n)):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

    def nCr_mod(n, r):
        res = 1
        while n or r:
            a, b = n % mod, r % mod
            if a < b:
                return 0
            res = res * fact[a] % mod * inv_fact[b] % mod * inv_fact[a - b] % mod
            n //= mod
            r //= mod
        return res

    return nCr_mod


def process(N, M):
 #   s = time.time()
    f = make_nCr_mod(mod=M)
    two_powers = [1]
    for i in range(401):
        two_powers.append((2*two_powers[-1]) % M)
    d = [[0 for i in range(N+1)] for i in range(N+1)]
    d[0][0] = 1
    for n in range(1, N+1):
        """
        the length of result
        """
        for a in range(1, n+1):
            """
            the number of consecutive numbers ending in n
            """
            entry = two_powers[a-1]
            if a==n:
                d[n][n]+=entry
            else:
                for l2 in range(1, n-a):
                    entry2 = d[n-a-1][l2]
                  #  print(a, l2, entry, entry2, f(l2+a, l2))
                    d[n][l2+a]+=(entry*entry2*f(l2+a, l2))
                    d[n][l2+a] = d[n][l2+a] % M
       # print(d[n][:n+1])
     #   print(n, time.time()-s)
    answer = 0
    for i in range(N+1):
    #    print(d[n][i])
        answer = (answer+d[n][i]) % M
    return answer

N, M = [int(x) for x in input().split()]
print(process(N, M))