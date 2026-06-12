# print ("Input n")
n = int(input())

# print ("Input the first soldiers cards (number then values)")
onecards = input().split()
onecards.pop(0)
for i in range(len(onecards)):
    onecards[i] = int(onecards[i])

# print ("Input the second soldiers cards (number then values)")
twocards = input().split()
twocards.pop(0)
for i in range(len(twocards)):
    twocards[i] = int(twocards[i])

startone = []
for i in range(len(onecards)):
    startone.append(onecards[i])
onelength = len(startone)

starttwo = []
for i in range(len(twocards)):
    starttwo.append(twocards[i])
twolength = len(starttwo)

plays = 0
while True:
    cone = onecards.pop(0)
    ctwo = twocards.pop(0)
    if (cone > ctwo):
        onecards.append(ctwo)
        onecards.append(cone)
    else:
        twocards.append(cone)
        twocards.append(ctwo)
    plays = plays + 1
    if (len(twocards) == 0):
        print (str(plays) + " 1")
        break
    if (len(onecards) == 0):
        print (str(plays) + " 2")
        break
    if ((onecards == startone and twocards == starttwo) or plays > math.factorial(10)):
        print (-1)
        break

    





