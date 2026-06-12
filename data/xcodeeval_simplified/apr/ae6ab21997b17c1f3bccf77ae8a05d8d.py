def getint():
    return [int(i) for i in input().split()]


def get():
    return int(input())


def getstr():
    return [i for i in input().split()]


def lower_bound(arr, x):
    left = -1
    right = len(arr)
    while left + 1 != right:
        mid = (left + right) // 2
        if arr[mid] < x:
            left = mid
        else:
            right = mid
    return right


def upper_bound(arr, x):
    left = -1
    right = len(arr)
    while left + 1 != right:
        mid = (left + right) // 2
        if arr[mid] <= x:
            left = mid
        else:
            right = mid
    return right


def solve():
    n = get()
    print(3 * n - 2)


def main():
    for _ in range(int(input())):
        solve()


if __name__ == "__main__":
    main()
