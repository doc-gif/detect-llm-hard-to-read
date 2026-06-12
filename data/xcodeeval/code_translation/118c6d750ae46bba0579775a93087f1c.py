input()
c = "".join(input().split()).strip('0')

if c.count('1') <= 1:
    print(c.count('1'))
else:
    print(eval("*".join([str(len(t)+1) for t in c.strip('1').split('1')])))