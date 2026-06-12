import sys


def get_all_factors(x):
    factors = []
    limit = int(x**0.5) + 1
    for i in range(1, limit):
        if x % i == 0:
            factors.append(i)
            if x // i != i:
                factors.append(x // i)
    return sorted(factors)


def main():
    MOD = 998244353
    n = int(input())
    dp = [0] * (n + 1)
    dp[1] = 1
    prefix_sum = 1
    for i in range(2, n + 1):
        dp[i] = prefix_sum + 2
        factors = get_all_factors(i)
        dp[i] += len(factors) - 2
        dp[i] %= MOD
        prefix_sum += dp[i]
        prefix_sum %= MOD
    print(dp[n])


input = sys.stdin.buffer.readline


def one_line_array_print(arr):
    print(" ".join(str(x) for x in arr))


def multi_line_array_print(arr):
    print("\n".join(str(x) for x in arr))


def multi_line_array_of_arrays_print(arr):
    print("\n".join(" ".join(str(x) for x in y) for y in arr))


def read_int_arr():
    return [int(x) for x in input().split()]


def make_arr(default_val_factory, dimension_arr):
    dv = default_val_factory
    da = dimension_arr
    if len(da) == 1:
        return [dv() for _ in range(da[0])]
    else:
        return [make_arr(dv, da[1:]) for _ in range(da[0])]


def query_interactive(i, j):
    print(f"? {i} {j}")
    sys.stdout.flush()
    return int(input())


def answer_interactive(ans):
    print("! " + " ".join(str(x) for x in ans))
    sys.stdout.flush()


inf = float("inf")
MOD = 10**9 + 7
for _ in range(1):
    main()
