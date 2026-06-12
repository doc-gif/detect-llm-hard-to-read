def pixel(input):
    red, green, blue = input.split()
    red = int(red)
    green = int(green)
    blue = int(blue)

    plist = [red,green,blue]
    plist.sort()

    lowestChet = is_chet(plist[0])
    midChet = is_chet(plist[1])

    if ((midChet + lowestChet) == 2) or ((midChet + lowestChet) == 0):
        return plist[1]
    else:
        return plist[2]


def is_chet(n):
    return 1 if n % 2 == 0 else 0
    
print(pixel(input()))