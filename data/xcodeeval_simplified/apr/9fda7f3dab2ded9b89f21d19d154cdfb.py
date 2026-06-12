MAX = 1000001
factor = [0] * (MAX + 1)


def generate_prime_factors():
    factor[1] = 1
    for i in range(2, MAX):
        factor[i] = i
    for i in range(4, MAX, 2):
        factor[i] = 2
    i = 3
    while i * i < MAX:
        if factor[i] == i:
            j = i * i
            while j < MAX:
                if factor[j] == j:
                    factor[j] = i
                j += i
        i += 1


def calculate_factors_count(n):
    if n == 1:
        return 1
    ans = 1
    dup = factor[n]
    c = 1
    j = n // factor[n]
    while j > 1:
        if factor[j] == dup:
            c += 1
        else:
            dup = factor[j]
            ans *= c + 1
            c = 1
        j //= factor[j]
    ans *= c + 1
    return ans


def calc(n):
    dp = [-1] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    pre = 2
    generate_prime_factors()
    for i in range(2, n + 1):
        dp[i] = pre + calculate_factors_count(i) - 1
        pre += dp[i]
    return dp[n] % 998244353


n = int(input())
print(calc(n))
