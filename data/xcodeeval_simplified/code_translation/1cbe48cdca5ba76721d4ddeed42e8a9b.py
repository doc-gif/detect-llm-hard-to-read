def main():
    height, node = read()
    node -= 1
    binary = bin(node)[2:].zfill(height)
    path = ""
    for i in range(height):
        if i > 0 and binary[i - 1] == "0":
            path += "1" if binary[i] == "0" else "0"
        else:
            path += binary[i]
    steps = 0
    for i in range(height):
        steps += 1
        if path[i] == "1":
            steps += (1 << (height - i)) - 1
    print(steps)
def read(mode=2):
    inputs = input().strip()
    if mode == 0:
        return inputs
    if mode == 1:
        return inputs.split()
    if mode == 2:
        return list(map(int, inputs.split()))
def write(s="\n"):
    if s is None:
        s = ""
    if isinstance(s, list):
        s = " ".join(map(str, s))
    print(s, end="")
write(main())