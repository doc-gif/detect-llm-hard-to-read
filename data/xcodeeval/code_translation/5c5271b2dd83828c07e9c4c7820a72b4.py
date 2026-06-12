w, h = map(int,input().split())
w1, h1 = map(int,input().split())
w2, h2 = map(int,input().split())
while h > 0 :
	w += h
	if h == h1:
		w -= w1
	if h == h2:
		w -= w2
	h -= 1
	w = max(0,w)
print(w)