def main():
    s = input()
    n, le = int(s), len(s)
    print((n + 1) * le - int('1' * le))


if __name__ == '__main__':
    main()
