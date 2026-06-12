def main():
  path = input()
  coordinate = [[0 for i in range(2)] for j in range(len(path)+1)]
  coordinate[0] = [0,0]
  left = 0
  right = 0
  up = 0
  down = 0

  for direction in path:
    if direction == 'U':
      up += 1
    elif direction == 'R':
     right += 1
    elif direction == 'D':
      down += 1
    elif direction == 'L':
      left += 1
  allDirections = [left,up,down,right]
  minDirection = min(allDirections)
  if minDirection == 0:
    allDirections.remove(0)
    minDirection = min(allDirections)
  i = minDirection + 1
  repeatingSequences = []
  while i < len(path):
    currentSet = set(path[i-minDirection - 1:i])
    if len(currentSet) == 1:
      repeatingSequences.append(path[i])
      i += minDirection
    else:
      i += 1
  if len(set(repeatingSequences)) == 3:
      print('BUG')
      return

  for i in range(2,len(path)):
    if path[i] != path[i-1] and path[i] != path[i-2] and path[i-1] != path[i-2]:
      print('BUG')
      return

  for i in range(0,len(path)):
    if i == 0:
      if path[i] == 'U':
        coordinate[i + 1][0] = 0
        coordinate[i + 1][1] = 1
      elif path[i] == 'R':
        coordinate[i + 1][0] = 1
        coordinate[i + 1][1] = 0
      elif path[i] == 'D':
        coordinate[i + 1][0] = 0
        coordinate[i + 1][1] = -1
      elif path[i] == 'L':
        coordinate[i + 1][0] = -1
        coordinate[i + 1][1] = 0
    else:
      if path[i] == 'U':
        coordinate[i + 1][0] = coordinate[i][0]
        coordinate[i + 1][1] += 1 + coordinate[i][1]
      elif path[i] == 'R':
        coordinate[i + 1][1] = coordinate[i][1]
        coordinate[i + 1][0] += 1 + coordinate[i][0]
      elif path[i] == 'D':
        coordinate[i + 1][0] = coordinate[i][0]
        coordinate[i + 1][1] += -1 + coordinate[i][1]
      elif path[i] == 'L':
        coordinate[i + 1][1] = coordinate[i][1]
        coordinate[i + 1][0] += -1 + coordinate[i][0]
  coordinateSet = list(set(map(tuple,coordinate)))

  if len(coordinate) == len(coordinateSet):
    print('OK')
  else:
    print('BUG')

main()