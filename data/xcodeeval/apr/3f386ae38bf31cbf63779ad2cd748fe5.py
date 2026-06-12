from collections import Counter

rep = input()
a = Counter({'B': 0, 'S': 0, 'C': 0})
a.update(rep)
rep = a['B'], a['S'], a['C']

inventory = Bi, Si, Ci = list(map(int, input().split(' ')))

for ingredient in range(3):
    if rep[ingredient] == 0:
        inventory[ingredient] = 0

price = list(map(int, input().split(' ')))

money = int(input())

output = 0


def make_sandwich():
    global output
    for idx in range(len(inventory)):
        inventory[idx] -= rep[idx]
    output += 1


while sum(inventory) != 0:
    if all([inventory[idx] >= rep[idx] for idx in range(len(inventory))]):
        make_sandwich()
        continue

    for ingredient in range(len(inventory)):
        if inventory[ingredient] < rep[ingredient] and money >= price[ingredient]:
            inventory[ingredient] += 1
            money -= price[ingredient]
            break

        if ingredient == 3:
            inventory = [0]

p = 0
for ingredient in range(3):
    p += rep[ingredient] * price[ingredient]

output += money // p
money -= p * output

print(output)
