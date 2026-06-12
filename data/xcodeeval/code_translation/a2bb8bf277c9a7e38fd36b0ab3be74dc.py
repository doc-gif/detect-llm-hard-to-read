inp = input().split(' ')
a = int(inp[0])
b = int(inp[1])

inp = input().split(' ')
x = int(inp[0])
y = int(inp[1])
z = int(inp[2])

foo = (2*x + y) - a
bar = (3*z + y) - b

out = 0
if foo > 0:
    out += foo
if bar > 0:
    out += bar
print(out)