from sys import stdin, stdout

garland = list(stdin.readline().rstrip("\n"))
remaining = garland.count("!")
kr = kb = ky = kg = 0
colors = {"R", "G", "B", "Y"}


def format_answer():
    return f"{kr} {kb} {ky} {kg}\n"


def get_neighbors(garland, idx):
    left = 0 if idx < 4 else idx - 3
    right = len(garland) - 1 if idx > len(garland) - 4 else idx + 3
    neighbors = set()
    for i in range(left, right + 1):
        if i != idx and garland[i] != "!":
            neighbors.add(garland[i])
    return neighbors


while remaining:
    for i in range(len(garland)):
        if garland[i] == "!":
            neighbor_set = get_neighbors(garland, i)
            possible = colors - neighbor_set
            if len(possible) == 1:
                color = possible.pop()
                garland[i] = color
                if color == "R":
                    kr += 1
                if color == "B":
                    kb += 1
                if color == "G":
                    kg += 1
                if color == "Y":
                    ky += 1
                remaining -= 1
stdout.write(format_answer())
