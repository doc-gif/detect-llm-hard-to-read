n = int(input())
a = int(input())
b = int(input())
c = int(input())
count = 0
while n >= a or n >= b:
    if b - c < a and n // b > 0:
        count = count + (n - c) // (b - c)
        n = n - (n - c) // (b - c) * (b - c)
    else:
        count = count + n // a
        n = n - n // a * a
print(count)