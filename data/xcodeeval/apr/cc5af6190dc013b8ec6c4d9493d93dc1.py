#!/usr/bin/env python3

a1 = int(input())
a2 = int(input())
k1 = int(input())
k2 = int(input())
n  = int(input())

minDeletedPlayers = 0
maxDeletedPlayers = 0

# Finding min deleted players
playersStates = []
for i in range(a1):
    playersStates.append(k1)
for i in range(a2):
    playersStates.append(k2)
memN = n
while memN > 0:
    # Finding max number
    maxNumber = -1
    itemId = 0
    for i, item in enumerate(playersStates):
        if item > maxNumber:
            maxNumber = item
            itemId = i
    playersStates[itemId] -= 1
    memN -= 1
for item in playersStates:
    if item <= 0:
        minDeletedPlayers += 1

# Finding max deleted players
playersStates = []
for i in range(a1):
    playersStates.append(k1)
for i in range(a2):
    playersStates.append(k2)
memN = n
while memN > 0:
    # Finding min number
    minNumber = 100500
    itemId = 0
    for i, item in enumerate(playersStates):
        if item < minNumber and item != 0:
            minNumber = item
            itemId = i
    playersStates[itemId] -= 1
    memN -= 1
for item in playersStates:
    if item <= 0:
        maxDeletedPlayers += 1

print(minDeletedPlayers, maxDeletedPlayers)
