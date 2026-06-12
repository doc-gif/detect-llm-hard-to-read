n = int(input())
m = input()
forward_to_south = 0
south_to_forward = 0
for i in range(1, len(m)):
    if m[i] == "F" and m[i - 1] == "S":
        forward_to_south += 1
    elif m[i] == "S" and m[i - 1] == "F":
        south_to_forward += 1
print("YES" if forward_to_south > south_to_forward else "NO")