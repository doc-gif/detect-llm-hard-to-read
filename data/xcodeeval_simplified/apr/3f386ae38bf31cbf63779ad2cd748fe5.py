from collections import Counter

recipe_str = input()
recipe_counter = Counter({"B": 0, "S": 0, "C": 0})
recipe_counter.update(recipe_str)
recipe = (recipe_counter["B"], recipe_counter["S"], recipe_counter["C"])
inventory = list(map(int, input().split()))
for i in range(3):
    if recipe[i] == 0:
        inventory[i] = 0
prices = list(map(int, input().split()))
money = int(input())
sandwiches_made = 0


def make_sandwich():
    global sandwiches_made
    for i in range(len(inventory)):
        inventory[i] -= recipe[i]
    sandwiches_made += 1


while sum(inventory) != 0:
    if all(inventory[i] >= recipe[i] for i in range(len(inventory))):
        make_sandwich()
        continue
    for i in range(len(inventory)):
        if inventory[i] < recipe[i] and money >= prices[i]:
            inventory[i] += 1
            money -= prices[i]
            break
        if i == 3:
            inventory = [0]
cost_per_sandwich = sum(recipe[i] * prices[i] for i in range(3))
sandwiches_made += money // cost_per_sandwich
money -= cost_per_sandwich * sandwiches_made
print(sandwiches_made)
