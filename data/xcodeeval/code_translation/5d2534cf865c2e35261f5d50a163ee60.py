# print ("Input digits and base for number one")
n1, b1 = (int(x) for x in input().split())
# print ("Input all the digits")
d1 = list(int(x) for x in input().split())
d1.reverse()

# print ("Input digits and base for number two")
n2, b2 = (int(x) for x in input().split())
# print ("Input all the digits")
d2 = list(int(x) for x in input().split())
d2.reverse()

# Compute base ten representation of number one
answer1 = 0
power1 = 1
for digit in d1:
    answer1 += digit*power1
    power1 *= b1
# print(answer1)

# Compute base ten representation of number two
answer2 = 0
power2 = 1
for digit in d2:
    answer2 += digit*power2
    power2 *= b2
# print(answer2)

if answer1 < answer2:
    print("<")
elif answer2 < answer1:
    print(">")
else:
    print("=")

    

