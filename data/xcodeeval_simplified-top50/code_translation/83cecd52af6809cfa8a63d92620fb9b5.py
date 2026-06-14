MOD = 10**9 + 7
def pow_mod(base, exponent):
    result = 1
    current = base
    while exponent != 0:
        if exponent % 2:
            result = (result * current) % MOD
        exponent //= 2
        current = (current * current) % MOD
    return result
def extended_gcd(a, b):
    assert a > 0 and b > 0
    original_a, original_b = a, b
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    assert a == original_a * x0 + original_b * y0
    assert b == original_a * x1 + original_b * y1
    while b != 0:
        quotient = a // b
        a, b = b, a - b * quotient
        x0, y0, x1, y1 = x1, y1, x0 - quotient * x1, y0 - quotient * y1
        assert a == original_a * x0 + original_b * y0
        assert b == original_a * x1 + original_b * y1
    return a, x0, y0
def solve(a, b, n, x):
    if a == 1:
        return (x + b * n) % MOD
    a_pow_n = pow_mod(a, n)
    gcd_val, inv_a_minus_1, _ = extended_gcd(a - 1, MOD)
    assert gcd_val == 1
    assert ((a - 1) * inv_a_minus_1) % MOD == 1
    result = (a_pow_n * x + b * (a_pow_n - 1) * inv_a_minus_1) % MOD
    return result
if __name__ == "__main__":
    a, b, n, x = map(int, input().split())
    print(solve(a, b, n, x))