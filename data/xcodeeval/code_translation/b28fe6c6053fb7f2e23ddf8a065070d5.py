pieces=''
result=0
for i in range(8):
    pieces+=input()
weight=dict(zip(list('QRBNPqrbnp.Kk'),[9,5,3,3,1,-9,-5,-3,-3,-1,0,0,0]))
for s in pieces:
    result+=weight[s]
if result>0:
    print('White')
elif result==0:
    print('Draw')
else:
    print('Black')