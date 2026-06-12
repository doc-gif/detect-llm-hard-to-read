pw = input()
forw = [input() for i in range(int(input()))]
revs = [(forw1[1] + forw2[0]) for forw1 in forw for forw2 in forw]
print("YES") if pw in forw + revs else print("NO")