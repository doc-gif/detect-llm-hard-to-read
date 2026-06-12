from itertools import permutations


def unlock(word, substring):
    if len(word) == 1:
        word = word + word
    perms = ["".join(w) for w in permutations(word)]
    for perm in perms:
        end = len(substring) - 1
        start = 0
        check = perm[: end + 1]
        while end != len(perm):
            if check == substring:
                return True
            end += 1
            start += 1
            check = perm[start : end + 1]
    return False


while True:
    try:
        pw = input()
        count = input()
        words = []
        for _ in range(int(count)):
            words.append(input())
        if unlock(words, pw):
            print("YES")
        else:
            print("NO")
    except EOFError:
        break
