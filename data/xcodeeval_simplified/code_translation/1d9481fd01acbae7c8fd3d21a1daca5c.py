inclusions = [2, 3, 5, 7, 30, 42, 70, 105]
exclusions = [6, 10, 14, 15, 21, 35, 210]
n = int(input())
count = 0
for divisor in inclusions:
    count += n // divisor
for divisor in exclusions:
    count -= n // divisor
print(n - count)