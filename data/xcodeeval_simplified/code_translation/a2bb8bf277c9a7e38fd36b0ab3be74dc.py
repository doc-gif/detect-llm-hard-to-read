inp = input().split()
a, b = map(int, inp)
inp = input().split()
x, y, z = map(int, inp)
foo = (2 * x + y) - a
bar = (3 * z + y) - b
out = 0
if foo > 0:
    out += foo
if bar > 0:
    out += bar
print(out)