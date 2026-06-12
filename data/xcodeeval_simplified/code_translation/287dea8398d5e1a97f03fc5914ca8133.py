def dominoes(m, n, k):
    fill_cols = (k // m) * 2
    left_cols = n - fill_cols
    left_doms = k % m
    if k * 2 > m * n:
        print("NO")
        return
    if left_doms == 0:
        if m % 2 == 0:
            print("YES")
        elif m * n == k * 2:
            print("YES")
        else:
            if left_cols % 2 == 0:
                stacks = left_cols // 2
                if stacks % 2 == 0:
                    fill_stacks = fill_cols // 2
                    extra_doms = fill_stacks * (m - 1)
                    print("YES" if extra_doms >= stacks else "NO")
                else:
                    print("NO")
            else:
                print("NO")
    else:
        if left_doms % 2 == 0:
            if m % 2 == 0:
                print("YES" if left_cols >= 2 else "NO")
            else:
                spread = left_doms - 1
                if left_cols % 2 == 0 and left_cols > 2:
                    stacks = (left_cols - 2) // 2
                    if stacks % 2 != 0:
                        if spread >= stacks:
                            print("YES")
                        else:
                            fill_stacks = fill_cols // 2
                            extra_doms = fill_stacks * (m - 1)
                            print("YES" if extra_doms >= (stacks - spread) else "NO")
                    else:
                        print("NO")
                else:
                    print("NO")
        else:
            if m % 2 == 0:
                print("NO")
            else:
                spread = left_doms - 1
                if left_cols % 2 == 0 and left_cols > 2:
                    stacks = (left_cols - 2) // 2
                    if stacks % 2 == 0:
                        if spread >= stacks:
                            print("YES")
                        else:
                            if (stacks - spread) % 2 == 0:
                                fill_stacks = fill_cols // 2
                                extra_doms = fill_stacks * (m - 1)
                                print(
                                    "YES" if extra_doms >= (stacks - spread) else "NO"
                                )
                            else:
                                print("NO")
                    else:
                        print("NO")
                else:
                    print("YES" if left_cols == 2 else "NO")
x = int(input())
for _ in range(x):
    m, n, k = map(int, input().split())
    dominoes(m, n, k)