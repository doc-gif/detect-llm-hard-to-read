def read_generator(transform):
    while True:
        parts = input().split()
        for part in parts:
            yield transform(part)
read_int = read_generator(int)
A1, B1, C1 = next(read_int), next(read_int), next(read_int)
A2, B2, C2 = next(read_int), next(read_int), next(read_int)
def cross(a, b, c, d):
    return a * d - b * c
def is_zero_vector(A, B):
    return A**2 + B**2 == 0
def line_intersect(A1, B1, C1, A2, B2, C2):
    if cross(A1, B1, A2, B2) == 0:
        if cross(A1, C1, A2, C2) == 0 and cross(B1, C1, B2, C2) == 0:
            return -1
        else:
            return 0
    else:
        return 1
def judge(A1, B1, C1, A2, B2, C2):
    if is_zero_vector(A1, B1) and C1 != 0:
        return 0
    if is_zero_vector(A2, B2) and C2 != 0:
        return 0
    if not is_zero_vector(A1, B1) and not is_zero_vector(A2, B2):
        return line_intersect(A1, B1, C1, A2, B2, C2)
    else:
        return -1
print(judge(A1, B1, C1, A2, B2, C2))