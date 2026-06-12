# http://codeforces.com/problemset/problem/272/A

number_people = int(input())
fingers = [int(x) for x in input().split()]

sum_fingers = sum(fingers)
fingers_hand = [1, 2, 3, 4, 5]
# s = [0] * (n + 1)
counter = 0

for i in fingers_hand:
    all_fingers = i + sum_fingers
    while all_fingers > 0:
        all_fingers -= (number_people + 1)
        if all_fingers == 1:
            counter += 1
            break

print(5 - counter)
