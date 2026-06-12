from math import sqrt

def tax(n):
    if n == 4:
        return 2
    if n < 4:
        return 1
    prime_lst = [i for i in range(2, n+1)]
    pointer = 0
    while pointer != n-1:
        if prime_lst[pointer] == 0:
            pass
        else:
            multiple = prime_lst[pointer]
            temp = pointer
            while pointer <= n:
                pointer += multiple
                try:
                    prime_lst[pointer] = 0
                except IndexError:
                    pass
            pointer = temp
        pointer += 1
    primes = []
    for i in prime_lst:
        if i != 0:
            primes.append(i)
    count = 0
    lp = 0
    while n > 0:
        try:
            if n - primes[-1-lp] >= 0 and n-primes[-1-lp] != 1:
                n -= primes[-1-lp]
                count += 1
            else:
                lp += 1
        except IndexError:
            lp = 0
    return count


n = int(input())
print(tax(n))



