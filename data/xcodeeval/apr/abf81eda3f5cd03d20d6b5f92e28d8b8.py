tmp = input()


def can(s, t):
    if len(s) != len(t):
        return False
    if 'X' in t:
        for ch in range(10):
            if can(s, t.replace('X', str(ch))):
                return True
        return False
    for i in range(len(s)):
        if s[i] == t[i] or t[i] == '_':
            continue
        else:
            return False
    return True


if len(tmp) <= 4:
    x = 0
    answer = 0
    while len(str(x)) <= len(tmp):
        if can(str(x), tmp):
            answer += 1 
        x += 25
    print(answer)
    exit(0)


def get_prefix(pref):
    if pref[0] == '0':
        return 0
    answer = 1
    if pref[0] == '_':
        answer = 9
    for i in range(1, len(pref)):
        if pref[i] == '_':
            answer *= 10
    return answer

def get_suffix(suff):
    answer = 0
    for good in ['00', '25', '50']:
        if can(good, suff):
            answer += 1
    return answer


def get(t):
    if 'X' in t:
        answer = 0
        for x in range(10):
            answer += get(t.replace('X', str(x)))
        return answer


    if tmp[0] == '0':
        return 0
    
    pref = t[0:len(t) - 2]
    suff = t[len(t) - 2:len(t)]
    return get_prefix(pref) * get_suffix(suff)

print(get(tmp))
