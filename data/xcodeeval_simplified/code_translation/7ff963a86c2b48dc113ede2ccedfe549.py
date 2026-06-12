from sys import stdin, stdout
from math import factorial
def read_ints():
    return list(map(int, stdin.readline().strip().split()))
def comb(n, k):
    if n - k >= 0:
        return factorial(n) // factorial(k) // factorial(n - k)
    else:
        return 0
def main():
    n, m, k = read_ints()
    result = (comb(n - 1, 2 * k) * comb(m - 1, 2 * k)) % 1000000007
    stdout.write(str(result))
if __name__ == "__main__":
    main()