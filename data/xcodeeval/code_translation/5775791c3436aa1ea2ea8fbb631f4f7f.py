def palindromeString(n):
    s = str(n)
    myList = list(s)
    for i in range(0, len(s)):
        myList.append(s[len(s) - i - 1])
    return int(''.join(myList))
inputLine = input()
inputList = inputLine.split(' ')
k = int(inputList[0])
p = int(inputList[1])
sum = 0
for i in range(1, k + 1):
    sum += palindromeString(i)
print(sum % p)
