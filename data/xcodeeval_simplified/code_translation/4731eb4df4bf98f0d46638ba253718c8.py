mem = {}
def C(f, h, kf, kh, kf_init, kh_init):
    if f + h == 0:
        return 1
    key = (f, h, kf, kh)
    if key not in mem:
        mem[key] = F(f, h, kf, kh, kf_init, kh_init) + H(f, h, kf, kh, kf_init, kh_init)
    return mem[key]
def F(f, h, kf, kh, kf_init, kh_init):
    if f > 0 and kf > 0:
        return C(f - 1, h, kf - 1, kh_init, kf_init, kh_init)
    return 0
def H(f, h, kf, kh, kf_init, kh_init):
    if h > 0 and kh > 0:
        return C(f, h - 1, kf_init, kh - 1, kf_init, kh_init)
    return 0
f, h, kf_init, kh_init = map(int, input().split())
print(C(f, h, kf_init, kh_init, kf_init, kh_init) % 100000000)