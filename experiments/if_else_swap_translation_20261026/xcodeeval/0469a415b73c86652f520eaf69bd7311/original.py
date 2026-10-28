n = int(input())
input_string = input()

map = {}

for i in range(0, len(input_string)):
    if input_string[i] in map:
        map[input_string[i]]+=1
    else:
        map[input_string[i]]=1


if len(map) == 3:
    print("BGR")


if len(map) == 2:
    sum = 0
    check = False
    check_key = ""
    other_key = ""
    for key in map.keys():
        sum += map[key]

        if map[key] == 1:
            check = True
            check_key = key
        else:
            other_key = key
    
    if sum == 2:
        if 'G' not in map:
            print("G")
        if 'R' not in map:
            print("R")
        if 'B' not in map:
            print("B")
    else:
        if check == True:
            if other_key == "R" and check_key == "G":
                print("BG")
            if other_key == "B" and check_key == "G":
                print("GR")
            if other_key == "B" and check_key == "R":
                print("GR")
            if other_key == "G" and check_key == "R":
                print("BR")
            if other_key == "R" and check_key == "B":
                print("BG")
            if other_key == "G" and check_key == "B":
                print("BR")    
        else:
            print("BGR")

if len(map) == 1:
    for key in map.keys():
        print(key)

    
