import string

def Correct(word):
    up = 0
    lo = 0
    flo = 0
    new = ''
    alpha = list(string.ascii_lowercase)
    ALPHA = list(string.ascii_uppercase)
    dic_one = {}
    dic_two = {}
    for i in range(0,26):
        dic_one[ALPHA[i]] = alpha[i]
    for j in range(0,26):
        dic_two[alpha[j]] = ALPHA[j] 
    l = list(word)
    for m in range(len(word)):
        for k in range(0,26):
            if l[m] == ALPHA[k]:
                up = up + 1
            elif l[0] == alpha[k]:
                flo = 1
    if l[0] == l[1]:
        if up == len(word):
            for m in range(0,len(word)):
                l[m] = dic_one[l[m]]
    elif up == len(word) and l[0] != l[1]:
        for m in range(1,len(word)):
            l[m] = dic_one[l[m]]
    elif flo == 1 and up == len(word)-1:
        l[0] = dic_two[l[0]]
        for m in range(1,len(word)):
            l[m] = dic_one[l[m]]
    else:
        return word
    for n in range(len(word)):
        new = new + l[n]
    return new

word = str(input())
print(Correct(word))