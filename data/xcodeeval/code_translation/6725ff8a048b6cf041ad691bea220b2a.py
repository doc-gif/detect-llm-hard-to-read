start, stop = input().split()
n = int(input())

d = {'v': 2 , '<': 3, '^':0, '>':1}

if (d[start] + n) % 4 == d[stop]:
    clockwise = True
else:
    clockwise = False

if (d[start] - n) % 4 == d[stop]:
    counter_clockwise = True
else:
    counter_clockwise = False


if counter_clockwise and clockwise:
    print('undefined')
elif clockwise:
    print('cw')
else:
    print('ccw')
