__copyright__ = ""
__author__ = "Son-Huy TRAN"
__email__ = "sonhuytran@gmail.com"
__doc__ = ""
__version__ = "1.0"
def main() -> int:
    n, d = map(int, input().split())
    costs = sorted(int(word) for word in input().split())
    m = int(input())
    if m <= n:
        profit = sum(costs[:m])
    else:
        profit = sum(costs) - (m - n) * d
    print(profit)
    return 0
if __name__ == "__main__":
    exit(main())