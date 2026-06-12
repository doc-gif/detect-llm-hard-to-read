def zip_sorted(a, b):
    a, b = zip(*sorted(zip(a, b)))
    sorted(zip(a, b), key=lambda x: x[1])
    return a, b


a = [int(n) for n in input().split()]
b = [int(n) for n in input().split()]
c = [int(n) for n in input().split()]
count = 0
for i in range(10**5):
    for j in range(10**5):
        a[0] = i
        b[1] = j
        if sum(a) == sum(b):
            c[2] = sum(a) - (b[1] + a[0])
            if (
                sum(c)
                == sum(a)
                == sum(b)
                == (c[0] + b[0] + a[0])
                == (c[1] + b[1] + a[1])
                == (c[1] + b[1] + a[1])
            ):
                count = 1
                break
    if count == 1:
        break
print(*a)
print(*b)
print(*c)
