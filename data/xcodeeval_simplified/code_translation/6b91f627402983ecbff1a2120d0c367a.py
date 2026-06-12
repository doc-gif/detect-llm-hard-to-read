def distance_to_point(x, y, d):
    if y == 0 or x == d:
        return x + y
    return 4 * d - x - y
d, x1, y1, x2, y2 = map(int, input().split())
dist1 = distance_to_point(x1, y1, d)
dist2 = distance_to_point(x2, y2, d)
difference = abs(dist1 - dist2)
print(min(difference, 4 * d - difference))