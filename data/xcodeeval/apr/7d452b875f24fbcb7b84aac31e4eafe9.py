#http://codeforces.com/problemset/problem/868/A

from itertools import permutations

def unlock(word,substring):
    if len(word) == 1:
        word = word + word
    perms = ["".join(w) for w in permutations(word)]
    for perm in perms:
        end = len(substring)-1
        start = 0
        check = perm[:end+1]
        #print(check)
        while end != len(perm):
            if check == substring:
                return True
            end += 1
            start += 1
            check = perm[start:end+1]
            #print(check)
    return False
        
    print(perms)


#print(unlock(["ah","oy","to","ha"],"ya"))
#print(unlock(["ht","tp"],"hp"))
#print(unlock(["ah"],"ha"))


while True:
    try:
        pw = input()
        count = input()
        words = []
        for i in range(int(count)):
            words.append(input())
        if unlock(words,pw):
            print("YES")
        else:
            print("NO")
    except EOFError:
        break
