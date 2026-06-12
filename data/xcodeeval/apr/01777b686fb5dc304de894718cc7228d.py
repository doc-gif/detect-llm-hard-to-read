def main(s):
    rst = 0
    legal_single = ['X', '_', '0']
    for ls in legal_single:
        if ls == s: return 1
    if len(s) < 2 or s.startswith('0'): return rst
    legal_ends = ['X', '_', '0', '5']
    if s[-1] not in legal_ends: return rst
    legal_2nds = ['X', '_', '0', '2', '5', '7']
    if s[-2] not in legal_2nds: return rst
    if s.endswith('XX'): return main(s.replace('X', '0'))
    elif s.endswith('X_'):
        rst += main(s.replace('X', '0')[:-1] + '0')
        rst += main(s.replace('X', '2')[:-1] + '5')
        rst += main(s.replace('X', '5')[:-1] + '0')
        rst += main(s.replace('X', '7')[:-1] + '5')
        return rst
    elif s.endswith('_X'):
        rst += main((s[:-2] + '00').replace('X', '0'))
        rst += main((s[:-2] + '25').replace('X', '5'))
        rst += main((s[:-2] + '50').replace('X', '0'))
        rst += main((s[:-2] + '75').replace('X', '5'))
        return rst
    elif s.endswith('__'):
        rst += main((s[:-2] + '00'))
        rst += main((s[:-2] + '25'))
        rst += main((s[:-2] + '50'))
        rst += main((s[:-2] + '75'))
        return rst
    elif 'X' in s[-2:] or '_' in s[-2:]:
        #Xnum, numX
        # _num, num_
        if 'X' in s[-2:]:
            if s[-2] == 'X': legal_2nds = ['2', '7']
            else: legal_2nds = ['0', '5']
            for l2 in legal_2nds: rst += main(s.replace('X', l2))
        elif '_' in s[-2:]:
            legal_2nds = ['0', '5', '2', '7']
            for l2 in legal_2nds: rst += main(s[:-2] + s[-2:].replace('_', l2)) 
        return rst
    # _ and X not in the last two number
    if not s[-2:] in ['00', '25', '50', '75']: return 0
    _num = s.count('_')
    X_num = s.count('X')
    if s.startswith('_'):
        rst += 9 * pow(10, (_num - 1)) * (10 if X_num > 0 else 1)
    elif s.startswith('X'): rst += 9 * pow(10, _num)
    elif '_' in s: rst += pow(10, _num) * (10 if X_num > 0 else 1)
    elif 'X' in s: rst += 10
    else: rst += 1 if int(s) % 25 == 0 else 0
    return rst


if __name__ == "__main__":
    s = input()
    rst = main(s)
    print(rst)