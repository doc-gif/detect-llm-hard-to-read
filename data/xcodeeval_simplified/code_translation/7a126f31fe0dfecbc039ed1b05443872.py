k = int(input())
b = input()
c = input()
d = input()
e = input()
s = b + c + d + e
digit_counts = [0] * 10
for char in s:
    if char == "0":
        digit_counts[0] += 1
    elif char == "1":
        digit_counts[1] += 1
    elif char == "2":
        digit_counts[2] += 1
    elif char == "3":
        digit_counts[3] += 1
    elif char == "4":
        digit_counts[4] += 1
    elif char == "5":
        digit_counts[5] += 1
    elif char == "6":
        digit_counts[6] += 1
    elif char == "7":
        digit_counts[7] += 1
    elif char == "8":
        digit_counts[8] += 1
    elif char == "9":
        digit_counts[9] += 1
valid_count = 0
for count in digit_counts:
    if count <= k * 2:
        valid_count += 1
if valid_count == 10:
    print("YES")
else:
    print("NO")