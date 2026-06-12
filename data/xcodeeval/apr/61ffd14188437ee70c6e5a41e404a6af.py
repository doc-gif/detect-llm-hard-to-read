from sys import stdin, stdout
# kr,kb,ky,kg

garland = list(stdin.readline()[:-1])
disabed = garland.count('!')

kr, kb, ky, kg = 0, 0, 0, 0
control = set(['R', 'G', 'B', 'Y'])


def format_answer():
    return str(kr) + ' ' + str(kb) + ' ' + str(ky) + ' ' + str(kg) + '\n'


def get_nei(garland, index):
    nei = set()
    left_index = 0 if index < 4 else index - 3
    right_index = len(garland) - 1 if index > len(garland) - 4 else index + 3
    for nei_index in range(left_index, right_index + 1):
        if not index == nei_index and garland[nei_index] != '!':
            nei.add(garland[nei_index])
    return nei

neighbours = {}

while disabed:

    for index in range(len(garland)):
        if garland[index] == '!':
            nei = get_nei(garland, index)
            diff = control.difference(nei)
            if len(diff) == 1:
                color = diff.pop()
                if color == 'R':
                    garland[index] = 'R'
                    kr += 1
                if color == 'B':
                    garland[index] = 'B'
                    kb += 1
                if color == 'G':
                    garland[index] = 'G'
                    kg += 1
                if color == 'Y':
                    garland[index] = 'Y'
                    ky += 1
                disabed -= 1

stdout.write(format_answer())