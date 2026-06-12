import itertools

def countZeroes(s):
    ret = 0
    for i in s:
        if i != '0':
            break
        ret += 1
    return ret

def stupid(n):
    ansMax = 0
    bn1 = n
    bn2 = n
    for n1 in itertools.permutations(n):
        for n2 in itertools.permutations(n):
            val = str(int(''.join(n1)) + int(''.join(n2)))[::-1]
            cnt = countZeroes(val)
            if cnt > ansMax:
                ansMax = cnt
                bn1 = ''.join(n1)
                bn2 = ''.join(n2)
    return (bn1, bn2)

def solution(n):
    ansMax = n.count('0')
    bestN1 = n.replace('0', '') + ansMax * '0'
    bestN2 = n.replace('0', '') + ansMax * '0'

    for i in range(1, 10):
        cnt1 = [n.count(str(j)) for j in range(10)]
        cnt2 = [n.count(str(j)) for j in range(10)]

        if cnt1[i] == 0 or cnt2[10 - i] == 0:
            continue
        cnt1[i] -= 1
        cnt2[10 - i] -= 1
        curN1 = str(i)
        curN2 = str(10 - i)
        ansCur = 1
        for j in range(10):
            addend = min(cnt1[j], cnt2[9 - j])
            ansCur += addend
            
            cnt1[j] -= addend
            cnt2[9 - j] -= addend

            curN1 += str(j) * addend
            curN2 += str(9 - j) * addend

        if cnt1[0] > 0 and cnt2[0] > 0:
            addend = min(cnt1[0], cnt2[0])
            ansCur += addend

            cnt1[0] -= addend
            cnt2[0] -= addend

            curN1 = '0' * addend + curN1
            curN2 = '0' * addend + curN2

        if ansCur > ansMax:
            ansMax = ansCur
            f = lambda x: str(x[0]) * x[1]
            bestN1 = ''.join(map(f, enumerate(cnt1))) + curN1[::-1]
            bestN2 = ''.join(map(f, enumerate(cnt2))) + curN2[::-1]

    return (bestN1, bestN2)


for n in range(1, 100500):
    answer = map(int, stupid(str(n)))
    candidate = map(int, solution(str(n)))

    if countZeroes(str(sum(answer))[::-1]) != countZeroes(str(sum(candidate))[::-1]):
        print('Wrong on test', n)
        print('Answer is', stupid(str(n)))
        print('Output is', solution(str(n)))
        break
