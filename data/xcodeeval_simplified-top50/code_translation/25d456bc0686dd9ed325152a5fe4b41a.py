n = int(input())
k = int(input())
A = int(input())
B = int(input())
mans = 0
if k == 1:
    print((n - 1) * A)
else:
    while n != 1:
        if n % k == 0:
            next_n = n // k
            cost = (n - next_n) * A
            mans += min(cost, B)
            n = next_n
        else:
            x = n - n % k
            if x == 0:
                mans += (n - 1) * A
                n = 1
            else:
                mans += (n - x) * A
                n = x
    print(mans)