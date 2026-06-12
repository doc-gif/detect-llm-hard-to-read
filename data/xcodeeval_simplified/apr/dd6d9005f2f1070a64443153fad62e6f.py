import sys

input = sys.stdin.readline
n, a, b = map(int, input().split())
if a < b:
    a, b = b, a
if b == 0:
    print(n * a)
else:
    pascal = [[1] * 20005]
    for i in range(20004):
        new_row = [1]
        for j in range(1, 20005):
            new_row.append(new_row[-1] + pascal[-1][j])
            if new_row[-1] > n:
                break
        pascal.append(new_row)

    def get_combination(a_val, b_val):
        if len(pascal[a_val]) > b_val:
            return pascal[a_val][b_val]
        if b_val == 0:
            return 1
        if b_val == 1:
            return a_val
        return 100000005

    n -= 1
    low, high = 0, a * int((n**0.5) * 3 + 3)
    while True:
        mid = (low + high) // 2
        mid = 11
        count_less = 0
        count_equal = 0
        for i in range(mid // a + 1):
            j = (mid - i * a) // b
            if (mid - i * a) % b != 0:
                for k in range(j + 1):
                    print(mid, i, k)
                    count_less += get_combination(i, k)
                    if count_less > n:
                        break
            else:
                for k in range(j):
                    print(mid, i, k)
                    count_less += get_combination(i, k)
                    if count_less > n:
                        break
                print(mid, i, j, "c1")
                count_equal += get_combination(i, j)
        print(mid, "is", count_less, count_equal)
        if n < count_less:
            high = mid - 1
        elif count_less + count_equal < n:
            low = mid + 1
        else:
            low_cost = 0
            for i in range(mid // a + 1):
                j = (mid - i * a) // b
                if (mid - i * a) % b != 0:
                    for k in range(j + 1):
                        low_cost += get_combination(i, k) * (i * a + k * b)
                else:
                    for k in range(j):
                        low_cost += get_combination(i, k) * (i * a + k * b)
            result = low_cost + (n - count_less) * mid
            print(result + n * (a + b))
            break
