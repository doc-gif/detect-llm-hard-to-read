cube = [-1] + list(map(int, input().split()))
def ok(cube):
    counter = 0
    last = cube[1]
    for i in cube:
        if i == -1:
            continue
        elif last == i:
            counter += 1
        else:
            if counter != 4:
                return False
            else:
                counter = 1
                last = i
    return True
def rotl(cube):
    cube_n = cube[:]
    cube_n[1], cube_n[2], cube_n[3], cube_n[4] = cube[3], cube[1], cube[4], cube[2]
    cube_n[5], cube_n[6] = cube[17], cube[18]
    cube_n[17], cube_n[18] = cube[21], cube[22]
    cube_n[21], cube_n[22] = cube[13], cube[14]
    cube_n[13], cube_n[14] = cube[5], cube[6]
    return cube_n
def rotr(cube):
    cube_n = cube[:]
    cube_n[1], cube_n[2], cube_n[3], cube_n[4] = cube[2], cube[4], cube[1], cube[3]
    cube_n[5], cube_n[6] = cube[13], cube[14]
    cube_n[17], cube_n[18] = cube[5], cube[6]
    cube_n[21], cube_n[22] = cube[17], cube[18]
    cube_n[13], cube_n[14] = cube[21], cube[22]
    return cube_n
def next(cube):
    cube_n = cube[:]
    cube_n[1:9] = cube[5:13]
    cube_n[9:13] = cube[24], cube[23], cube[22], cube[21]
    cube_n[13], cube_n[14], cube_n[15], cube_n[16] = (
        cube[14],
        cube[16],
        cube[13],
        cube[15],
    )
    cube_n[17], cube_n[18], cube_n[19], cube_n[20] = (
        cube[19],
        cube[17],
        cube[20],
        cube[18],
    )
    cube_n[21:25] = cube[4], cube[3], cube[2], cube[1]
    return cube_n
def next2(cube):
    cube_n = cube[:]
    cube_n[1:5] = cube[3], cube[1], cube[4], cube[2]
    cube_n[5:9] = cube[17:21]
    cube_n[9:13] = cube[10], cube[12], cube[9], cube[11]
    cube_n[13:17] = cube[5:9]
    cube_n[17:21] = cube[21:25]
    cube_n[21:25] = cube[13:17]
    return cube_n
def main(cube):
    return ok(rotl(cube)) or ok(rotr(cube))
for _ in range(4):
    cube = next(cube)
    if main(next(cube)):
        print("YES")
        exit()
for _ in range(4):
    cube = next2(cube)
    if main(next(cube)):
        print("YES")
        exit()
print("NO")