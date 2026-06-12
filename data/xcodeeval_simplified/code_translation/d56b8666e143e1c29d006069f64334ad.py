def list_to_string(sequence):
    return "".join(sequence)
num_index = []
x = input()
nums = [int(n) for n in x.split()]
letters = input()
letter_list = list(letters)
for _ in range(nums[1]):
    for j in range(nums[0] - 1):
        if letter_list[j] == "B" and letter_list[j + 1] == "G":
            num_index.append(j)
    for idx in num_index:
        letter_list[idx], letter_list[idx + 1] = letter_list[idx + 1], letter_list[idx]
    num_index.clear()
print(list_to_string(letter_list))