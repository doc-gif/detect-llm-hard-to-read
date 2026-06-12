def make_s(lst):
    while True:
        lst.sort()
        for i in range(len(lst) - 1):
            if lst[i] == lst[i + 1]:
                lst[i] -= 1
                break
        else:
            break
    return sum([x for x in lst if x > 0])


n = int(input())
a = [int(i) for i in input().split()]
print(make_s(a))