def main():
    n, m = map(int, input().strip().split())
    temp = 1
    while m != n:
        if m % 10 == 0:
            print(0)
            return
        temp *= m
        m -= 1
    print(temp % 10)
if __name__ == "__main__":
    main()