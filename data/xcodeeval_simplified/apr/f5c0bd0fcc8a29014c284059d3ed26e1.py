arr = list(map(int, input().split()))
t1 = 0
t2 = 0


def main():
    global t1, t2, arr
    i = 0
    arr = sorted(arr)
    tmp = arr
    while i < len(tmp):
        t1 += tmp[i]
        tmp.pop(i)
        t1 += tmp[i]
        tmp.pop(i)
        j = 0
        while j < tmp:
            t1 += tmp[j]
            tmp.pop(j)
            for c in tmp:
                t2 += c
            j += 1
        i += 1
    while i < len(arr):
        t1 += arr[i]
    if t1 == t2:
        print("YES")
    else:
        print("NO")


if __name__ == "__main__":
    main()
