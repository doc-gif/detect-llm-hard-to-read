w, m = map(int, input().split())
def can_reduce(m, w):
    while m != 0:
        remainder = (m + 1) % w
        if remainder == 0:
            m = (m + 1) // w
        elif remainder < 3:
            m = m // w
        else:
            return False
    return True
if w == 2 or can_reduce(m, w):
    print("YES")
else:
    print("NO")