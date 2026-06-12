string = input()
dash_count = string.count("-")
circle_count = string.count("o")
if circle_count == 0 or dash_count % circle_count == 0:
    print("YES")
else:
    print("NO")