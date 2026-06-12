
def determine(arr, poss, seen):
	if seen[arr[0]][arr[1]][arr[2]]:
		return poss[arr[0]][arr[1]][arr[2]]
	else:
		seen[arr[0]][arr[1]][arr[2]] = True
		if arr[0] >= 2:
			a = [arr[0] - 1, arr[1], arr[2]]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		if arr[1] >= 2:
			a = [arr[0], arr[1]-1, arr[2]]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		if arr[2] >= 2:
			a = [arr[0], arr[1], arr[2]-1]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		if arr[0] >= 1 and arr[1] >= 1:
			a = [arr[0] - 1, arr[1]-1, arr[2]+1]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		if arr[0] >= 1 and arr[2] >= 1:
			a = [arr[0] - 1, arr[1]+1, arr[2]-1]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		if arr[1] >= 1 and arr[2] >= 1:
			a = [arr[0] + 1, arr[1] - 1, arr[2] - 1]
			p1 = determine(a, poss, seen)
			for i in range(3):
				if p1[i] == True: 
					poss[arr[0]][arr[1]][arr[2]][i] = True
		return poss[arr[0]][arr[1]][arr[2]]

a = int(input())
s = input()

arr = [0, 0, 0]

for i in range(len(s)):
	if s[i] == "B":
		arr[0] += 1
	elif s[i] == "G":
		arr[1] += 1
	else:
		arr[2] += 1

b = arr[0]
g = arr[1]
r = arr[2]

seen = [[[False for i in range(r+g+b+1)] for i in range(r+g+b+1)] for i in range(r+g+b+1)]
seen[0][0][0] = True
poss = [[[[False, False, False] for i in range(r+g+b+1)] for i in range(r+g+b+1)] for i in range(r+g+b+1)]
poss[0][0][0] = [False, False, False]

seen[1][0][0] = True
poss[1][0][0][0] = True

seen[0][1][0] = True
poss[0][1][0][1] = True

seen[0][0][1] = True
poss[0][0][1][2] = True
a = determine(arr, poss, seen)

t = ""
if a[0] == True:
	t += "B"
if a[1] == True:
	t += "G"
if a[2] == True:
	t += "R"

print(t)

