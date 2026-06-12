# print("Input n")
n = int(input())

threepower = 27
sevenpower = 7
count = 1
while (count < n):
    threepower = (threepower * 27) % (1000000000+7)
    sevenpower = (sevenpower * 7) % (1000000000+7)
    count += 1
answer = threepower - sevenpower
if answer < 0:
    answer += 1000000000+7
print(answer)
