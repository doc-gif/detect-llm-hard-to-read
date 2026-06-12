s = input()
"""if s == "V":
    print(0)
    exit()
if s == "VK" or s == "VV" or s == "KK":
    print(1)
    exit()
beg = s.count("VK")
m = beg
kk = s.count("KK")
kv = s.count("KV")
vv = s.count("VV")

buf = s[:]
f = s[:]
while kk:
    c = f.find("KK")
    if c != -1:
        f = f[:c] + "--" + f[c + 1:]
        tmp = buf[:c] + "VK" + buf[c + 1:]
        if tmp.count("VK") > m:
            m = buf.count("VK")
    kk -= 1

buf = s[:]
f = s[:]
while kv:
    c = f.find("KV")
    if c != -1:
        f = f[:c] + "--" + f[c + 1:]
        tmp = buf[:c] + "VK" + buf[c + 1:]
        if tmp.count("VK") > m:
            m = tmp.count("VK")
    kv -= 1

buf = s[:]
f = s[:]
while vv:
    c = f.find("VV")
    if c != -1:
        f = f[:c] + "--" + f[c + 1:]
        tmp = buf[:c] + "VK" + buf[c + 1:]
        if tmp.count("VK") > m:
            m = buf.count("VK")
    vv -= 1

print(m)"""
print (max((s[:i] + x + s[i+1:]).count("VK") for x in "VK" for i in range(len(s))))