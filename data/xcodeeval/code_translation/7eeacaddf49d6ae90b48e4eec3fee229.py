fin = input()

a, b, c = map(int, fin.split())
rings = 0

for ring in range(c):
  rings = rings + (2 * a + 2 * b - 4)

  a = a - 4
  b = b - 4

print(rings)
