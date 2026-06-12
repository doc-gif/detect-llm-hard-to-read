import fileinput
i=0
costMatrix = []

for line in fileinput.input():
    if i<3:
        costMatrix.append([int(i) for i in line.split()])
        i+=1
    else:
        n = int(line)


def switchC(MAT):
    SW = [[0]*3 for i in range(3)]
    SW[0][1]=MAT[0][2]
    SW[0][2]=MAT[0][1]
    SW[1][0]=MAT[1][0]
    SW[2][0]=MAT[1][0]
    SW[1][2] = MAT[2][1]
    SW[2][1] = MAT[1][2]
    return SW

def switchC2(MAT):
    SW = [[0]*3 for i in range(3)]
    SW[0][1]=MAT[1][0]
    SW[0][2]=MAT[1][2]
    SW[1][0]=MAT[0][1]
    SW[2][0]=MAT[2][1]
    SW[1][2] = MAT[0][2]
    SW[2][1] = MAT[2][0]
    return SW

def switchC3(MAT):
    SW = [[0]*3 for i in range(3)]
    SW[0][1]=MAT[2][1]
    SW[0][2]=MAT[2][0]
    SW[1][0]=MAT[1][2]
    SW[2][0]=MAT[0][2]
    SW[1][2] = MAT[1][0]
    SW[2][1] = MAT[0][1]
    return SW

def hashMAT(n,MAT):
    M = max(n,MAT[0][1],MAT[0][2],MAT[1][0],MAT[1][2],MAT[2][0],MAT[2][1])
    hashed = n + M*MAT[0][1]+M**2*MAT[0][2]+M**3*MAT[1][0]+M**4*MAT[1][2]+M**5*MAT[2][0]+M**6*MAT[2][1]
    return hashed

a = {}

def SmallY(n,MAT):
    h = hashMAT(n,MAT)
    isIN = h in list(a.keys())
    if n == 1:
        if isIN:
            return a[h]
        else:
            a[h] = min(MAT[0][2], MAT[0][1]+MAT[1][2])
            return a[h]
    else:
        if isIN:
            return a[h]
        else:
            a[h] = min(MAT[0][2]+SmallY(n-1,switchC(MAT))+SmallY(n-1,switchC2(MAT)),MAT[0][1]+MAT[1][2]+2*SmallY(n-1,MAT)+SmallY(n-1,switchC3(MAT)))
            return a[h]

print(SmallY(n,costMatrix))

