import datetime as DT

def bus(a, t_a, b, t_b, t):

	t1 = DT.datetime.strptime(t, '%H:%M')
	t2 = DT.datetime(1900, 1, 1)
	t_start = ((t1 - t2).total_seconds() / 60.0) - 300
	t_end = t_start + t_a

	t_elapsed = 0
	z = 0

	while(t_elapsed <= 23 * 60 + 59 - 300):
		start = t_elapsed
		end = start + t_b
		if(max(t_start, start) < min(t_end, end)):
			z += 1
		t_elapsed += b
	return z
	

if __name__ == "__main__":
    a = input().split(' ')
    b = input().split(' ')
    t = input()
    print(bus(int(a[0]), int(a[1]), int(b[0]), int(b[1]), t))
