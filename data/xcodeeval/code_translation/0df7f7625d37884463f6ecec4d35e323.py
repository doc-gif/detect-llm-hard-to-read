a=input().replace(' ','')
print('YES' if a.strip().lower()[-2] in 'aeiouy' else "NO")