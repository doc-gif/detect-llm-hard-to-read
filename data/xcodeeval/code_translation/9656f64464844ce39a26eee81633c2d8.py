x, y = map(int, input().split())
a, b = map(int, input().split())
c, d = map(int, input().split())

def solve():
  for X, Y in [(x, y), (y, x)]:
    for A, B in [(a, b), (b, a)]:
      for C, D in [(c, d), (d, c)]:
        if A + C <= X and max(B, D) <= Y:
          return 'YES'
  return 'NO'

print(solve())
