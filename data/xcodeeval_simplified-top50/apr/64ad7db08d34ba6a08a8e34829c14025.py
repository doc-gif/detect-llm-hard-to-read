def pixel(input):
    red, green, blue = input.split()
    pixels = [int(red), int(green), int(blue)]
    RED = 0
    GREEN = 1
    BLUE = 2
    battles = 0
    while True:
        if pixels[RED] == pixels[GREEN]:
            break
        if pixels[RED] == pixels[BLUE]:
            break
        if pixels[GREEN] == pixels[RED]:
            break
        if pixels[GREEN] == pixels[BLUE]:
            break
        if pixels[BLUE] == pixels[RED]:
            break
        if pixels[BLUE] == pixels[GREEN]:
            break
        lowest = get_min_key(pixels)
        if lowest == RED:
            f1, f2, w = GREEN, BLUE, RED
        elif lowest == GREEN:
            f1, f2, w = RED, BLUE, GREEN
        elif lowest == BLUE:
            f1, f2, w = RED, GREEN, BLUE
        pixels[f1] -= 1
        pixels[f2] -= 1
        pixels[w] += 1
        battles += 1
    min_battles = 0
    max_battles = 0
    min_pixels = pixels.copy()
    max_pixels = pixels.copy()
    lowest = get_min_key(pixels)
    if lowest == RED:
        f1, f2, w = GREEN, BLUE, RED
    elif lowest == GREEN:
        f1, f2, w = RED, BLUE, GREEN
    elif lowest == BLUE:
        f1, f2, w = RED, GREEN, BLUE
    while True:
        if len([x for x in max_pixels if x <= 0]) > 1:
            break
        if max_pixels[f1] == 0:
            f1, w = w, f1
        if max_pixels[f2] == 0:
            f2, w = w, f2
        max_pixels[f1] -= 1
        max_pixels[f2] -= 1
        max_pixels[w] += 1
        min_battles += 1
    highest = get_max_key(pixels)
    if highest == RED:
        f1, f2, w = GREEN, BLUE, RED
    elif highest == GREEN:
        f1, f2, w = RED, BLUE, GREEN
    elif highest == BLUE:
        f1, f2, w = RED, GREEN, BLUE
    while True:
        if len([x for x in min_pixels if x <= 0]) > 1:
            break
        if min_pixels[f1] == 0:
            f1, w = w, f1
        if min_pixels[f2] == 0:
            f2, w = w, f2
        min_pixels[f1] -= 1
        min_pixels[f2] -= 1
        min_pixels[w] += 1
        max_battles += 1
    total_min = battles + min_battles
    total_max = battles + max_battles
    return total_min if total_min < total_max else total_max


def get_max_key(pixels):
    max_key = 0
    max_val = pixels[max_key]
    for key, val in enumerate(pixels):
        if val > max_val:
            max_val = val
            max_key = key
    return max_key


def get_min_key(pixels):
    min_key = 0
    min_val = pixels[min_key]
    for key, val in enumerate(pixels):
        if val < min_val:
            min_val = val
            min_key = key
    return min_key


print(pixel(input()))
