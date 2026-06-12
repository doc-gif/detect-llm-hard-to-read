input()
w,s=set('aeiouy'),input()
print(''.join(c[0] for c in zip(s,'b'+s) if w<w|set(c)))