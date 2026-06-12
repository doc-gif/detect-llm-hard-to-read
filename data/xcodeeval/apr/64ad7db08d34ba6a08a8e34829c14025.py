def pixel(input):
    red, green, blue = input.split()
    pixels = [int(red), int(green), int(blue)]

    red = 0
    green = 1
    blue = 2

    battles = 0

    f1 = None
    f2 = None
    w = None


    while True:
        if pixels[red] == pixels[green]:
            break
        if pixels[red] == pixels[blue]:
            break
        if pixels[green] == pixels[red]:
            break
        if pixels[green] == pixels[blue]:
            break
        if pixels[blue] == pixels[red]:
            break
        if pixels[blue] == pixels[green]:
            break


        lowest = get_min_key(pixels)
        if lowest == red:
            f1 = green
            f2 = blue
            w = red
        elif lowest == green:
            f1 = red
            f2 = blue
            w = green
        elif lowest == blue:
            f1 = red
            f2 = green
            w = blue

        pixels[f1] -= 1
        pixels[f2] -= 1
        pixels[w] += 1
        battles += 1

    minBattles = 0
    maxBattles = 0
    minPixels = pixels.copy()
    maxPixels = pixels.copy()


    lowest = get_min_key(pixels)

    if lowest == red:
        f1 = green
        f2 = blue
        w = red
    elif lowest == green:
        f1 = red
        f2 = blue
        w = green
    elif lowest == blue:
        f1 = red
        f2 = green
        w = blue

    while True:
        is_mir = len([x for x in maxPixels if x <= 0]) > 1
        if is_mir:
            break

        if maxPixels[f1] == 0:
            tmp = w
            w = f1
            f1 = tmp

        if maxPixels[f2] == 0:
            tmp = w
            w = f2
            f2 = tmp

        maxPixels[f1] -= 1
        maxPixels[f2] -= 1
        maxPixels[w] += 1

        minBattles += 1

    highest = get_max_key(pixels)
    if highest == red:
        f1 = green
        f2 = blue
        w = red
    elif highest == green:
        f1 = red
        f2 = blue
        w = green
    elif highest == blue:
        f1 = red
        f2 = green
        w = blue

    while True:
        is_mir = len([x for x in minPixels if x <= 0]) > 1
        if is_mir:
            break

        if minPixels[f1] == 0:
            tmp = w
            w = f1
            f1 = tmp

        if minPixels[f2] == 0:
            tmp = w
            w = f2
            f2 = tmp

        minPixels[f1] -= 1
        minPixels[f2] -= 1
        minPixels[w] += 1

        maxBattles += 1

    return battles + minBattles if battles + minBattles < battles + maxBattles else battles + maxBattles

def get_max_key(pixels):
    maxKey = 0
    max = pixels[maxKey]
    for key, pixel in enumerate(pixels):
        if pixel > max:
            max = pixel
            maxKey = key

    return maxKey


def get_min_key(pixels):
    minKey = 0
    min = pixels[minKey]
    for key, pixel in enumerate(pixels):
        if pixel < min:
            min = pixel
            minKey = key

    return minKey
    
print(pixel(input()))