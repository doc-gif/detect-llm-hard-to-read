def mult_mod(a, b, m):
    c = [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
         [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]
    for i in range(2):
        for j in range(2):
            c[i][j] %= m
    return c

def pow_mod(n, m):
    p = [[1, 1],
         [1, 0]]

    a = [[1, 0],
         [0, 1]]

    while n:
        if n % 2:
            a = mult_mod(a, p, m)
        p = mult_mod(p, p, m)
        n /= 2
    return a

def fib(n, m):
    return pow_mod(n, m)[0]

def egcd(a, b):
    if b == 0:
        return 1, 0, a
    x1, y1, c = egcd(b, a % b)
    return y1, x1 - (a / b) * y1, c

def crt(a0, n0, a1, n1):
    if min(n0, n1) < 0:
        return 0, -1
    x, y, g = egcd(n0, n1)
    if (a0 - a1) % g:
        return 0, -1
    x *= (a1 - a0) / g
    y *= (a1 - a0) / g
    k = n1 * n0 / g
    return (n0 * x + a0) % k, k


# 2**13 ->   12288
# 5**8  -> 1562500
# 5**9  -> 7812500


def find(f, m, l):
    resp = []
    x0 = 0
    x1 = 1
    for i in range(l):
        if x0 == f % m:
            resp.append(i)
        x0, x1 = x1, (x0 + x1) % m
    return resp

f = input()
a = find(f, 2**13, 12288)
b = find(f, 5**9, 1562500)

if len(a) == 0 or len(b) == 0:
    print('-1')
else:
    ans = 10 ** 30
    fm = pow_mod(4800000000, 10 ** 13)
    for i in a:
        for j in b:
            a0, n0 = crt(i, 12288, j, 1562500)
            if n0 != -1:
                x1, x0 = fib(a0, 10 ** 13)
                if x0 == f:
                    ans = min(ans, a0)
                else:
                    a0 += n0
                    
                    x3 = (x1 * fm[0][0] + x0 * fm[1][0]) % 10 ** 13
                    x2 = (x1 * fm[0][1] + x0 * fm[1][1]) % 10 ** 13
                    while (x2,x3) != (x0, x1):
                        if x2 == f:
                            ans = min(ans, a0)
                            break
                        a0 += n0
                        x3, x2 = (x3 * fm[0][0] + x2 * fm[1][0]) % 10 ** 13, (x3 * fm[0][1] + x2 * fm[1][1]) % 10 ** 13
    if ans < 10 ** 30:
        print(ans)
    else:
        print(-1)