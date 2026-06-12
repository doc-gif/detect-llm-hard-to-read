n = int(input())
max_a = n // 1234567
max_b = n // 123456
found = False
for a in range(max_a + 1):
    for b in range(max_b + 1):
        remainder = n - (1234567 * a + 123456 * b)
        if remainder >= 0 and remainder % 1234 == 0:
            print("YES")
            found = True
            break
    if found:
        break
if not found:
    print("NO")