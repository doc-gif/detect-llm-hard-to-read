n, m, a = map(int, input().split())
nn = n // a + (1 if n % a != 0 else 0)
mm = m // a + (1 if m % a != 0 else 0)
print(nn * mm)