n, m = map(int, input().split())
if (m == 0 and n != 1) or m > 9 * n:
    print(-1, -1)
elif n == 1 and m == 0:
    print(0, 0)
else:
    min_num = 10 ** (n - 1)
    for i in range(m - 1):
        digit_position = i // 9
        min_num += 10**digit_position
    max_num = 0
    for i in range(m):
        digit_position = n - 1 - i // 9
        max_num += 10**digit_position
    print(min_num, max_num)