def val(line):
    vals = []
    current = ""
    for char in line:
        if char == " ":
            vals.append(current)
            current = ""
        else:
            current += char
    vals.append(current)
    return vals
data = input()
n, m = map(int, val(data))
result = n + int((n - 1) / (m - 1))
print(result)