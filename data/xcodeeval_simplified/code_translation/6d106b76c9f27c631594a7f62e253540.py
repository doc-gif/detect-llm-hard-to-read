def get(y, m, d):
    if m < 3:
        y -= 1
        m += 12
    return 365 * y + y // 4 - y // 100 + y // 400 + (153 * m - 457) // 5 + d - 306
date1 = input().split(":")
date2 = input().split(":")
y1, m1, d1 = map(int, date1)
y2, m2, d2 = map(int, date2)
print(abs(get(y1, m1, d1) - get(y2, m2, d2)))