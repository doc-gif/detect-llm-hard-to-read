def main(n, lst):
    if n == 1:
        return "YES"
    if lst[0] < lst[1]:
        status = 0
    elif lst[0] == lst[1]:
        status = 1
    else:
        status = 2
    for i in range(len(lst) - 1):
        if status == 0:
            if lst[i] == lst[i + 1]:
                status += 1
            if lst[i] > lst[i + 1]:
                status += 2
        if status == 1:
            if lst[i] > lst[i + 1]:
                status += 1
            if lst[i] < lst[i + 1]:
                return "NO"
        if status == 2:
            if lst[i] > lst[i + 1]:
                pass
            else:
                return "NO"
    return "YES"
n = eval(input())
lst = [eval(i) for i in input().split()]
print(main(n, lst))