#7A - Kalevitch and Chess
#We get the costumer's requested board: 8 lines of input
# W - white
# B - black
order = []
for i in range(8):
    order.append(input())
#Firstly, we create a variable allBlack (reference to an all-black row) and
    #set it to be true
allBlack = True
#We instantiate the count of strokes as zero
count = 0
#Now, we iterate through the board, row by row
for row in order:
    #If we find a row with all 8 swuares marked as black ('B')
    if row == "BBBBBBBB":
        #We clearly add 1 stroke to the count
        count += 1
    else:
        #else, we say that it's not an all-black row
        allBlack = False
#Let's assume that all of the board's squares are marked with 'B'
#It doesn't matter if we have already iterated through rows,
#it's allowed to over-paint a square when rows of black cross columns of black
#The next loop is actually to find columns of black squares
for i in range(8):
    count += 1
    for ii in range(8):   #This is the second loop, because we have a board of 8x8
        #If the square is marked with 'W', we bring the count one step back
        if order[ii][i] == "W":
            count -= 1
            break
#The simpliest case: if we got the count result to be 16 black squares,
            #we will subsequently need 8 strokes
        #We print this directly, just so our program wouldn't bother
        #to count the obvious and return a bigger count
if count == 16:
    print("8")
    #Else, we print the number of counts previously computed
else:
    print(count)