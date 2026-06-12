a = input()

p = a.count('4')
q = a.count('7')

if p > 0 and p >= q:
    print('4')
elif q > 0:
    print('7')
else:
    print('-1')
