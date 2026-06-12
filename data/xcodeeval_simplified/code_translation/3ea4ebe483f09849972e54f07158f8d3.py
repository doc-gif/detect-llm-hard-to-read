number_people = int(input())
fingers = [int(x) for x in input().split()]
sum_fingers = sum(fingers)
counter = 0
for i in range(1, 6):
    all_fingers = i + sum_fingers
    while all_fingers > 0:
        all_fingers -= number_people + 1
        if all_fingers == 1:
            counter += 1
            break
print(5 - counter)