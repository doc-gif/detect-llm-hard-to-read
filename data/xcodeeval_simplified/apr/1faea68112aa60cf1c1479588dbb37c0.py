import string

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
first_string = input()
second_string = input()
first_indices = []
second_indices = []
for char in first_string:
    if char in UPPERCASE:
        index = UPPERCASE.find(char)
        first_indices.append(index)
    elif char in LOWERCASE:
        index = LOWERCASE.find(char)
        first_indices.append(index)
for char in second_string:
    if char in UPPERCASE:
        index = UPPERCASE.find(char)
        second_indices.append(index)
    elif char in LOWERCASE:
        index = LOWERCASE.find(char)
        second_indices.append(index)
length = len(first_indices)
for i in range(length):
    if first_indices[i] == second_indices[i]:
        pass
    elif first_indices[i] < second_indices[i]:
        w -= 1
    elif first_indices[i] > second_indices[i]:
        w += 1
print(w)
