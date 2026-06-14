n, x, y = map(int, input().split())
a = list(map(int, input().split()))
ans_a = ans_b = 0
ans = True
for i in range(n // 2):
    left, right = a[i], a[n - i - 1]
    if left != right:
        if left == 2 or right == 2:
            if left == 0 or right == 0:
                ans_a += 1
            elif left == 1 or right == 1:
                ans_b += 1
        else:
            ans = False
            break
    else:
        if left == 2 and right == 2:
            if x < y:
                ans_a += 2
            else:
                ans_b += 2
if ans:
    middle_cost = 0
    if n % 2 == 1 and a[n // 2] == 2:
        middle_cost = min(x, y)
    print(ans_a * x + ans_b * y + middle_cost)
else:
    print(-1)