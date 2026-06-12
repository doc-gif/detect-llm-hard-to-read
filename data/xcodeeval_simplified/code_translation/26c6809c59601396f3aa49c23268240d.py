read = lambda: map(int, input().split())
k, n = read()
a = list(read())
cnt4 = k
cnt2 = 2 * k
for i in range(n):
    use = min(cnt4, a[i] // 4)
    a[i] -= use * 4
    cnt4 -= use
for i in range(n):
    use = min(cnt2, a[i] // 2)
    a[i] -= use * 2
    cnt2 -= use
freq = [0] * 20
for val in a:
    freq[min(val, 19)] += 1
use = min(cnt4, freq[3])
freq[3] -= use
cnt4 -= use
use = min(cnt4, freq[1], freq[2])
freq[1] -= use
freq[2] -= use
cnt4 -= use
use = min(cnt2, freq[2])
freq[2] -= use
cnt2 -= use
use = min(cnt2, freq[1])
freq[1] -= use
cnt2 -= use
use = min(cnt4, (freq[2] + 2) // 3 + int(freq[2] > 1))
freq[2] -= use + use // 2
cnt4 -= use
use = min(cnt4, freq[2])
freq[2] -= use
cnt4 -= use
use = min(cnt4, (freq[1] + 1) // 2)
freq[1] -= use * 2
cnt4 -= use
use = min(cnt4, freq[1])
freq[1] -= use
cnt4 -= use
print("YES" if sum(freq[1:]) == 0 else "NO")