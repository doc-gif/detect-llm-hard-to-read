l = list(map(int, input().split(" ")))
s = list(set(l))
m = max(list(map(lambda x: l.count(x), s)))
if m < 4:
    print("Alien")
elif m == 5 or len(s) == 3:
    print("Bear")
else:
    print("Elephant")
