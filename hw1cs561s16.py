# @author Sagar Makwana

#Function Definition

#Checks whether the input position can be sneaked or not.
#Returns a boolean
def isSneakable(currentBoardState, player , iPosition , jPosition):

    if iPosition-1 >= 0 and str(currentBoardState[iPosition-1][jPosition]) == player:
        return False
    elif iPosition+1 <= 4 and str(currentBoardState[iPosition+1][jPosition]) == player:
        return False
    elif jPosition-1 >= 0 and str(currentBoardState[iPosition][jPosition-1]) == player:
        return False
    elif jPosition+1 <= 4 and str(currentBoardState[iPosition][jPosition+1]) == player:
        return False

    return True

#Return the enemy of the input player
def getEnemy (player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

#Checks whether the position is occupied or not
def isOccupied(currentBoardState, iPosition, jPosition):
    if (currentBoardState[iPosition][jPosition] != '*'):
        return True
    else:
        return False

#Checks the outcome value on performing raid on the input position
def getRaidValue(currentBoardState, boardValues, player, iPosition, jPosition):
    raidValue = int(boardValues[iPosition][jPosition])
    enemyPlayer = getEnemy(player)

    if iPosition-1 >= 0 and currentBoardState[iPosition-1][jPosition] == enemyPlayer:
        raidValue += int(boardValues[iPosition-1][jPosition])

    if iPosition+1 <= 4 and currentBoardState[iPosition+1][jPosition] == enemyPlayer:
        raidValue += int(boardValues[iPosition+1][jPosition])

    if jPosition-1 >= 0 and currentBoardState[iPosition][jPosition-1] == enemyPlayer:
        raidValue += int(boardValues[iPosition][jPosition-1])

    if jPosition+1 <= 4 and currentBoardState[iPosition][jPosition+1] == enemyPlayer:
        raidValue += int(boardValues[iPosition][jPosition+1])

    return raidValue



#Initialisation of the variables
gameTask = 0
gamePlayer = 0
gameEnemyPlayer = 0
gameCutOff = 0

#Initialization of Maximization Variables
maxValue = -1
maxMove = -1  # maxMove {1:Raid, 2:Sneak}
maxIPosition = -1
maxJPosition = -1

boardValues = []
boardState = []

#Reading the input file
inputFile = open('input.txt')

#Reading the game task player and cutoff
gameTask  = inputFile.readline().strip()
gamePlayer = inputFile.readline().strip()
gameCutOff = inputFile.readline().strip()
gameEnemyPlayer = getEnemy(gamePlayer)

#Reading the board grid values
for i in range(0, 5):
    line = inputFile.readline()
    boardValues.append(line.split())

#Reading the current board status
for i in range(0, 5):
    l = list(inputFile.readline().strip())
    boardState.append(l)

inputFile.close()



#The Game Logic starts here.

print 'Before GBFS:'
print boardState

#Check the status of each position
for i in range(0,5):
    for j in range(0,5):
        #If the position is not occupied check if its sneakable.
        if (not(isOccupied(boardState,i,j))):
            if (isSneakable(boardState,gamePlayer,i,j)):
                if (int(boardValues[i][j]) > maxValue):
                    maxValue = int(boardValues[i][j])
                    maxIPosition = i
                    maxJPosition = j
                    maxMove = 2

        # If the position is occupied by the player
        elif (boardState[i][j] == gamePlayer):

            if (i-1 >= 0 and not(isOccupied(boardState,i-1,j))):
                raidValue = getRaidValue(boardState,boardValues,gamePlayer,i-1,j)
                if (raidValue > maxValue):
                    maxValue = raidValue
                    maxIPosition = i-1
                    maxJPosition = j
                    maxMove = 1

            if (j-1 >= 0 and not(isOccupied(boardState,i,j-1))):
                raidValue = getRaidValue(boardState,boardValues,gamePlayer,i,j-1)
                if (raidValue > maxValue):
                    maxValue = raidValue
                    maxIPosition = i
                    maxJPosition = j-1
                    maxMove = 1

            if (j+1 <= 4 and not(isOccupied(boardState,i,j+1))):
                raidValue = getRaidValue(boardState,boardValues,gamePlayer,i,j+1)
                if (raidValue > maxValue):
                    maxValue = raidValue
                    maxIPosition = i
                    maxJPosition = j+1
                    maxMove = 1

            if (i+1 <= 4 and not(isOccupied(boardState,i+1,j))):
                raidValue = getRaidValue(boardState,boardValues,gamePlayer,i+1,j)
                if (raidValue > maxValue):
                    maxValue = raidValue
                    maxIPosition = i+1
                    maxJPosition = j
                    maxMove = 1


if (maxMove == 1): #Raid
    #Do raid operation

    boardState[maxIPosition][maxJPosition] = gamePlayer

    if (maxIPosition-1 >= 0 and boardState[maxIPosition-1][maxJPosition] == gameEnemyPlayer):
        boardState[maxIPosition-1][maxJPosition] = gamePlayer

    if (maxJPosition-1 >= 0 and boardState[maxIPosition][maxJPosition-1] == gameEnemyPlayer):
        boardState[maxIPosition][maxJPosition-1] = gamePlayer

    if (maxJPosition+1 <=4  and boardState[maxIPosition][maxJPosition+1] == gameEnemyPlayer):
        boardState[maxIPosition][maxJPosition+1] = gamePlayer

    if (maxIPosition+1 <= 4 and boardState[maxIPosition+1][maxJPosition] == gameEnemyPlayer):
        boardState[maxIPosition+1][maxJPosition] = gamePlayer

    print 'Raid Operation performed at ',maxIPosition,' ',maxJPosition

elif (maxMove == 2):
    #Do sneak operation
    boardState[maxIPosition][maxJPosition] = gamePlayer

    print 'Sneak operation performed',maxIPosition,' ',maxJPosition

print 'After GBFS:'
print boardState

outputFile = open('next_state.txt','w')

for i in range(0,5):
    outputFile.write(''.join(boardState[i]))
    outputFile.write('\n')