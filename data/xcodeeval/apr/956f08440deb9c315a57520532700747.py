temp = input().split(" ")
maxLength, initialCount = [int(x) for x in temp]

resultSet = {1: [], 2: []}
dataSet = dict()
for i in range(initialCount):
    temp = input().split(" ")
    a, b = [x for x in temp]
    dataSet[a] = b
    resultSet[1] = b
    resultSet[2] = a

def populate(toValue):
    fromValues = []
    if len(toValue) == 1:
        for key, value in dataSet.items():
            if value == toValue and not key in fromValues:
                fromValues.append(key)
    else:
        process = toValue[:1]
        tail = toValue[1:]
        firstPart = populate(process)
        if len(firstPart) > 0:
            fromValues = fromValues + [x + tail for x in firstPart if (not x + tail in fromValues and (not x + tail in dataSet.keys()))]
    return fromValues
count = 0
currents = ["a"]
currentCount = 1
while currentCount < maxLength:
    buffer = []
    for current in currents:
        result = populate(current)
        for key in result:
            dataSet[key] = current
        buffer = buffer + result
    if len(buffer) > 0:
        currentCount += 1
        currents = buffer
        if currentCount == maxLength:
            count = len(buffer)
    else:
        break
print(count)
