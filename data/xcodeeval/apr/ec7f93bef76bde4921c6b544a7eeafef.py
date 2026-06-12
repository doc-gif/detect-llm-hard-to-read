for t in range(int(input())):
    n = int(input())
    if not n % 2:
        print(f'{n // 2} {n // 2}')
    else:
        ans = [True] * ((n // 2) + 1)
        idx = 1
        for i in range(3, (n // 2) + 1):
            if not ans[i] or not i % 2:
                continue
            if n % i > 0:
                ans[i] = False
                for j in range(2, ((n // 2) + 1) // i):
                    ans[i * j] = False
            elif n % i == 0:
                idx = i
                break
        # print(ans, idx)
        if idx == 1:
            print(f'{1} {n - 1}')
        else:
            print(f'{n // idx} {n - n // idx}')


# for t in range(int(input())):
#     n = int(input())
#     a = list(map(int, input().split()))
#     cnt = 0
#     i = 0
#     while i < n:
#         while i < n and a[i] == i + 1:
#             i += 1
#         j = i
#         while i < n and a[i] != i + 1:
#             i += 1
#         cnt += 1 if j - i else 0
#     print(cnt)
