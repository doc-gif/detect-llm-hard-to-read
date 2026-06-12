def main():
    n = int(input()) % 6
    x = int(input())
    patterns = [[0, 1, 2, 2, 1, 0], [1, 0, 0, 1, 2, 2], [2, 2, 1, 0, 0, 1]]
    for i, pattern in enumerate(patterns):
        if pattern[n] == x:
            print(i)
main()