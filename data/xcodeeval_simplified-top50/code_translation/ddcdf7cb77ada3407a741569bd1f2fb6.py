import itertools
def king():
    n = int(input())
    s = input()
    star_positions = []
    for i, char in enumerate(s):
        if char == "*":
            star_positions.append(i + 1)
    if len(star_positions) < 5:
        print("no")
        return
    for combination in itertools.combinations(star_positions, 5):
        sorted_combination = sorted(combination)
        differences = []
        for i in range(4):
            differences.append(sorted_combination[i + 1] - sorted_combination[i])
        if len(set(differences)) == 1:
            print("yes")
            return
    print("no")
king()