x1, y1, z1 = input().split()
x2, y2, z2 = input().split()
has_common_coordinate = (x1 == x2) or (y1 == y2) or (z1 == z2)
print("YES" if has_common_coordinate else "NO")