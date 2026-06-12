total = []

def excg(s, p1, p2, new):
    if p1 > p2:
        (p1, p2) = (p2, p1)
    #print ('--', s, p1, p2, new)
    s = s[:p1] + s[p1+1:p2] + s[p2+1:]
    #print (s + new)
    #input()
    return s + new

def calc(s):
    global total

    if len(s) == 1:
        if s[0] not in total:
            total += s[0]
        return

    pr = s.find('R')
    pr2 = s.find('R', pr + 1)

    pg = s.find('G')
    pg2 = s.find('G', pg + 1)

    pb = s.find('B')
    pb2 = s.find('B', pb + 1)

    if pr+pr2>0: calc(excg(s, pr, pr2, 'R'))
    if pg+pg2>0: calc(excg(s, pg, pg2, 'G'))
    if pb+pb2>0: calc(excg(s, pb, pb2, 'B'))

    if pr+pb>0: calc(excg(s, pr, pb, 'G'))
    if pr+pg>0: calc(excg(s, pr, pg, 'B'))
    if pb+pg>0: calc(excg(s, pb, pg, 'R'))

    
n = input()
s = input()

calc(s)

for b in total: print(b, end='')
