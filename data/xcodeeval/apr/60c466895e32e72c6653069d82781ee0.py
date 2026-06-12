n = int(input())

dice1 = [int(i) for i in input().split()]
dice2 = [int(i) for i in input().split()]
dice3 = [int(i) for i in input().split()]

h = [0] * 100000

for i in dice1:
  h[i]+=1
  for j in dice2:
    h[j]+=1
    for k in dice3:
      h[k]+=1
      #pairs
      num = (i*10) + j
      h[num]+=1
      num = (j*10) + i
      h[num]+=1
      num = (i*10) + k
      h[num]+=1
      num = (k*10) + i
      h[num]+=1
      num = (k*10) + j
      h[num]+=1
      num = (j*10) + k
      h[num]+=1
      #triplets
      num = (i*100) + (j*10) + k
      h[num]+=1
      num = (i*100) + (k*10) + j
      h[num]+=1
      num = (k*100) + (i*10) + j
      h[num]+=1
      num = (k*100) + (j*10) + i
      h[num]+=1
      num = (j*100) + (i*10) + k
      h[num]+=1
      num = (j*100) + (k*10) + i
      h[num]+=1

h = h[1:]

print(len(h[:h.index(0)]))
