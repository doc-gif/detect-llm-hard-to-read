
def val(line):
    vals = []
    l = ''
    for i in line:
        if i == ' ':
            vals.append(l)
            l = ''
        else:
            l += i
    vals.append(l)
    return vals

data = input()
n,m = map(int,val(data))
result = n + int((n-1)/(m-1))
print(result)
