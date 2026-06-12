from math import log2 as log


def gen(a, b, c):
    return [f"{a}^{b}^{c}", f"{a}^{c}^{b}", f"({a}^{b})^{c}", f"({a}^{c})^{b}"]


def f(val):
    return log(val)


def calc1(a, b, c):
    return [
        c * f(b) + f(f(a)),
        b * f(c) + f(f(a)),
        f(b * c) + f(f(a)),
        f(c * b) + f(f(a)),
    ]


def calc2(a, b, c):
    return [a**b**c, a**c**b, a ** (b * c), a ** (c * b)]


def build(a, b, c):
    labels, values = [], []
    if a > 1:
        labels += gen("x", "y", "z")
        values += calc1(a, b, c)
    if b > 1:
        labels += gen("y", "x", "z")
        values += calc1(b, a, c)
    if c > 1:
        labels += gen("z", "x", "y")
        values += calc1(c, a, b)
    return labels, values


def build2(a, b, c):
    labels, values = [], []
    if a > 1:
        labels += gen("x", "y", "z")
        values += calc2(a, b, c)
    if b > 1:
        labels += gen("y", "x", "z")
        values += calc2(b, a, c)
    if c > 1:
        labels += gen("z", "x", "y")
        values += calc2(c, a, b)
    return labels, values


x, y, z = (float(t) for t in input().strip().split())
labels, values = build(x, y, z)
if not labels:
    labels, values = build2(x, y, z)
print(labels[values.index(max(values))])
