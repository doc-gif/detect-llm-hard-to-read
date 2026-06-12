def main():
    n = int(input())
    min1, max1 = [int(t) for t in input().split()]
    min2, max2 = [int(t) for t in input().split()]
    min3, max3 = [int(t) for t in input().split()]

    s1 = min(max1, n - min2 - min3)
    s2 = min(max2, n - s1 - min3)
    s3 = n - s1 - s2

    print(' '.join(str(s) for s in [s1, s2, s3]))


if __name__ == '__main__':
    main()
