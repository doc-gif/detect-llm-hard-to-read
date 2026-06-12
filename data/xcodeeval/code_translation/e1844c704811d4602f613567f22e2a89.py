#  L R L R L R L R L R L R
# 0 1 2 2 1 0 0 1 2 2 1 0 ...
# 1 0 0 1 2 2 1 0 0 1 2 2 ...
# 2 2 1 0 0 1 2 2 1 0 0 1 ...



def main():
    n = int(input())
    x = int(input())

    patterns = [ [0, 1, 2, 2, 1, 0], [1, 0, 0, 1, 2, 2], [2, 2, 1, 0, 0, 1] ]

    n %= 6
    for i, pattern in enumerate(patterns):
        if pattern[n] == x:
            print(i)

main()
