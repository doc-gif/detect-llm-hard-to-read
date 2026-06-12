def reflection(num):
    tmp = []
    numlist = list(str(num))
    for el in numlist:
        i = int(el)
        ni = 9-i
        if ni == 0 and len(tmp) == 0:
            continue
        tmp.append(str(ni))
    if not tmp:
        return 0
    return int("".join(tmp))
    
def solve(l, r):
    result = 0
    result = max(result, l*reflection(l))
    result = max(result, r*reflection(r))

    start = 0
    while 5*(10**start) <= l:
        start += 1
    
    while 5*(10**start) <= r:
        cur_num = 5*(10**start)
        result = max(result, cur_num*reflection(cur_num))
        start += 1
    return result


l, r = map(int, input().split())
result = solve(l, r)
print(result)
