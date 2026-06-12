import sys

MOD = 10**9 + 7


def main():
    n = int(sys.stdin.readline().strip())
    t = 1
    m = 1
    for i in range(1, n + 2):
        t = (t * ((n + i + 1) % MOD)) % MOD
        m = (m * (i % MOD)) % MOD
    print((t // m - 1) % MOD)


if __name__ == "__main__":
    main()
