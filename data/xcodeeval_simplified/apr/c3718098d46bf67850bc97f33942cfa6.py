import sys


def get_int_list():
    return list(map(int, input().split()))


def scale_by_four(x):
    return x * 4


s1_raw = get_int_list()
s2_raw = get_int_list()
s1_scaled = list(map(scale_by_four, s1_raw))
s1_points = [(s1_scaled[i], s1_scaled[i + 1]) for i in range(0, 8, 2)]
s2_scaled = list(map(scale_by_four, s2_raw))
s2_points = [(s2_scaled[i], s2_scaled[i + 1]) for i in range(0, 8, 2)]
s1_x = [p[0] for p in s1_points]
s1_x_min = min(s1_x)
s1_x_max = max(s1_x)
s1_y = [p[1] for p in s1_points]
s1_y_min = min(s1_y)
s1_y_max = max(s1_y)
s2_x_plus_y = [p[0] + p[1] for p in s2_points]
s2_x_plus_y_min = min(s2_x_plus_y)
s2_x_plus_y_max = max(s2_x_plus_y)
s2_x_minus_y = [p[0] - p[1] for p in s2_points]
s2_x_minus_y_min = min(s2_x_minus_y)
s2_x_minus_y_max = max(s2_x_minus_y)
for x in range(-800, 801):
    for y in range(-800, 801):
        if s1_x_min < x < s1_x_max and s1_y_min < y < s1_y_max:
            if (
                s2_x_plus_y_min < x + y < s2_x_plus_y_max
                and s2_x_minus_y_min < x - y < s2_x_minus_y_max
            ):
                print("YES")
                sys.exit()
print("NO")
