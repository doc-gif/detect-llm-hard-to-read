def prime(n):
    if n == 1:
        return 0
    for j in range(2, int(pow(n, 0.5)) + 1):
        if n % j == 0:
            return 0
    return 1


a, b = map(int, input().split())
if prime(a) == 1 and prime(b) == 1:
    for i in range(a + 1, b+1):
        if prime(i) == 0:
            #print(i)
            continue
        else:
           # print(i)
            if i == b:
                print('YES')
                break
            else:
                print('NO')
                break
else:
    print('NO')
