import string


def Correct(word):
    uppercase_count = 0
    first_is_lower = 0
    lowercase_letters = list(string.ascii_lowercase)
    uppercase_letters = list(string.ascii_uppercase)
    to_lower = {}
    to_upper = {}
    for i in range(26):
        to_lower[uppercase_letters[i]] = lowercase_letters[i]
    for i in range(26):
        to_upper[lowercase_letters[i]] = uppercase_letters[i]
    chars = list(word)
    for m in range(len(word)):
        for k in range(26):
            if chars[m] == uppercase_letters[k]:
                uppercase_count += 1
            elif chars[0] == lowercase_letters[k]:
                first_is_lower = 1
    if chars[0] == chars[1]:
        if uppercase_count == len(word):
            for m in range(len(word)):
                chars[m] = to_lower[chars[m]]
    elif uppercase_count == len(word) and chars[0] != chars[1]:
        for m in range(1, len(word)):
            chars[m] = to_lower[chars[m]]
    elif first_is_lower == 1 and uppercase_count == len(word) - 1:
        chars[0] = to_upper[chars[0]]
        for m in range(1, len(word)):
            chars[m] = to_lower[chars[m]]
    else:
        return word
    new = ""
    for n in range(len(word)):
        new = new + chars[n]
    return new


word = str(input())
print(Correct(word))
