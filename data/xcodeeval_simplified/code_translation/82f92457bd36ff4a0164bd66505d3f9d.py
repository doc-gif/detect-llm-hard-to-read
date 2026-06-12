a, b = map(int, input().split())
if b == 1:
    print(a)
elif b == 2:
    if a % 2 == 0:
        print(a // 2)
    else:
        print(a - 1)
else:
    even_binary = bin(b + 1)[3:]
    even_length = len(even_binary)
    best_even = ((a - int(even_binary, 2)) // (2**even_length)) * 2
    odd_binary = bin(b)[2:]
    odd_length = len(odd_binary)
    best_odd = ((a - b) // (2**odd_length)) * 2 + 1
    print(best_even if best_even > best_odd else best_odd)