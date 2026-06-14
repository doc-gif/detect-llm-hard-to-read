def is_right_triangle(sides):
    x1, y1, x2, y2, x3, y3 = sides
    a = (x1 - x2) ** 2 + (y1 - y2) ** 2
    b = (x1 - x3) ** 2 + (y1 - y3) ** 2
    c = (x2 - x3) ** 2 + (y2 - y3) ** 2
    return a and b and c and (a + b == c or a + c == b or b + c == a)
def classify_triangle(sides):
    if is_right_triangle(sides):
        return "RIGHT"
    for i in range(6):
        sides[i] -= 1
        if is_right_triangle(sides):
            return "ALMOST"
        sides[i] += 2
        if is_right_triangle(sides):
            return "ALMOST"
        sides[i] -= 1
    return "NEITHER"
points = list(map(int, input().split()))
print(classify_triangle(points))