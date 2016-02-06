# @author Sagar Makwana

#---------------------------------------Function Definitions------------------------------------------------

#Evaluation Function
def getEvaluationValue(boardState, boardValues, gamePlayer ):

    playerValue = 0
    enemyPlayerValue = 0

    gameEnemyPlayer = getEnemy(gamePlayer)
    for i in range(0,5):
        for j in range(0,5):
            if boardState[i][j] == gamePlayer:
                playerValue += int(boardValues[i][j])
            elif boardState[i][j] == gameEnemyPlayer:
                enemyPlayerValue += int(boardValues[i][j])

    return playerValue-enemyPlayerValue

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

#Prints the log for minimax
#@param boardPosition:Alphanumeric position on the board ex.A1,B2
def printLog(boardPosition, depth, evaluationUtility, traverseLogFile):

    if evaluationUtility == float('inf'):
        traverseLogFile.write(boardPosition+','+str(depth)+','+'Infinity')
    elif evaluationUtility == -float('inf'):
        traverseLogFile.write(boardPosition+','+str(depth)+','+'-Infinity')
    else:
        traverseLogFile.write(boardPosition+','+str(depth)+','+str(evaluationUtility))

    traverseLogFile.write('\n')

#Prints the log for alpha beta pruning
#@param boardPosition:Alphanumeric position on the board ex.A1,B2
def printABLog(boardPosition, depth, evaluationUtility, alpha, beta, traverseLogFile):

    if evaluationUtility == float('inf'):
        evaluationUtility = 'Infinity'
    elif evaluationUtility == -float('inf'):
        evaluationUtility = '-Infinity'

    if alpha == float('inf'):
        alpha = 'Infinity'
    elif alpha == -float('inf'):
        alpha = '-Infinity'

    if beta ==  float('inf'):
        beta = 'Infinity'
    elif beta == -float('inf'):
        beta = '-Infinity'

    traverseLogFile.write(boardPosition+','+str(depth)+','+str(evaluationUtility)+','+str(alpha)+','+str(beta))

    traverseLogFile.write('\n')

#Returns the alphanumeric board position
def getBoardPosition(iPosition, jPosition):
    return str(chr(65+jPosition))+str(iPosition+1)

#Returns a boolean whether the board is full or not.
def isBoardFull (boarState):
    for i in range(0,5):
        for j in range(0,5):
            if not(isOccupied(boardState,i,j)):
                return False
    return True

#----------------------------------------Algorithms--------------------------------------------------------

#Algorithm for Greedy BFS algorithm
def GBFS(gameTask, gamePlayer, gameEnemyPlayer,gameCutOff, boardValues, boardState):

    #Initialization of Maximization Variables
    maxValue = -1
    maxMove = -1  # maxMove {1:Raid, 2:Sneak}
    maxIPosition = -1
    maxJPosition = -1

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

#Algorithm for Minimax
#Constant parameters :{boardValue, gamePlayer, cutoffDepth, traverseLogFile }
def MINIMAX(boardState, boardValues, gamePlayer, player, cutoffDepth, currentDepth, iSelfPosition, jSelfPosition, traverseLogFile):

    evaluationUtility = -99

    #Base Condition
    if currentDepth == cutoffDepth or isBoardFull(boardState):
        evaluationUtility = getEvaluationValue(boardState,boardValues,gamePlayer)
        if currentDepth != 0:
            printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile)
        else:
            printLog('root',currentDepth,evaluationUtility,traverseLogFile)
        return evaluationUtility

    #Recursive Element
    if currentDepth%2 == 0:
        evaluationUtility = -float('inf')
    else:
        evaluationUtility = float('inf')

    if (currentDepth != 0):
        printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile)
    else:
        printLog("root",currentDepth,evaluationUtility,traverseLogFile)

    for i in range(0,5):
        for j in range(0,5):

            if (not(isOccupied(boardState,i,j))):
                #Initializing the new board state for next move
                newBoardState = [eachRow[:] for eachRow in boardState]
                if (isSneakable(boardState,player,i,j)):
                    newBoardState[i][j] = player
                else:
                    enemyPlayer = getEnemy(player)
                    newBoardState[i][j] = player

                    if (i-1 >= 0 and newBoardState[i-1][j] == enemyPlayer):
                        newBoardState[i-1][j] = player

                    if (j-1 >= 0 and newBoardState[i][j-1] == enemyPlayer):
                        newBoardState[i][j-1] = player

                    if (j+1 <=4  and newBoardState[i][j+1] == enemyPlayer):
                        newBoardState[i][j+1] = player

                    if (i+1 <= 4 and newBoardState[i+1][j] == enemyPlayer):
                        newBoardState[i+1][j] = player

                childUtility = MINIMAX(newBoardState,boardValues,gamePlayer,getEnemy(player),cutoffDepth,currentDepth+1,i,j,traverseLogFile)

                if currentDepth%2 == 0:
                    if (childUtility > evaluationUtility):
                        evaluationUtility = childUtility
                else:
                    if (childUtility < evaluationUtility):
                        evaluationUtility = childUtility

                if currentDepth != 0:
                    printLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,traverseLogFile)
                else:
                    printLog("root",currentDepth,evaluationUtility,traverseLogFile)

    return evaluationUtility

#Algorithm for Alpha Beta Pruning
#Constant parameters :{boardValue, gamePlayer, cutoffDepth, traverseLogFile }
def ABPrune (boardState, boardValues, gamePlayer, player, cutoffDepth, currentDepth, iSelfPosition, jSelfPosition, alpha, beta, traverseLogFile ):

    evaluationUtility = -99

    #Base Condition
    if currentDepth == cutoffDepth or isBoardFull(boardState):
        evaluationUtility = getEvaluationValue(boardState,boardValues,gamePlayer)

        if (currentDepth != 0):
            printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile)
        else:
            printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile)

        return evaluationUtility

    #Recursive Element
    if currentDepth%2 == 0:
        evaluationUtility = -float('inf')
    else:
        evaluationUtility = float('inf')

    if (currentDepth != 0):
        printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile)
    else:
        printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile)

    isBreak = False
    for i in range(0,5):
        if isBreak == True:
            break

        for j in range(0,5):

            if (not(isOccupied(boardState,i,j))):
                #Initializing the new board state for next move
                newBoardState = [eachRow[:] for eachRow in boardState]
                if (isSneakable(boardState,player,i,j)):
                    newBoardState[i][j] = player
                else:
                    enemyPlayer = getEnemy(player)
                    newBoardState[i][j] = player

                    if (i-1 >= 0 and newBoardState[i-1][j] == enemyPlayer):
                        newBoardState[i-1][j] = player

                    if (j-1 >= 0 and newBoardState[i][j-1] == enemyPlayer):
                        newBoardState[i][j-1] = player

                    if (j+1 <=4  and newBoardState[i][j+1] == enemyPlayer):
                        newBoardState[i][j+1] = player

                    if (i+1 <= 4 and newBoardState[i+1][j] == enemyPlayer):
                        newBoardState[i+1][j] = player

                childUtility = ABPrune(newBoardState,boardValues,gamePlayer,getEnemy(player),cutoffDepth,currentDepth+1,i,j,alpha,beta,traverseLogFile)

                if currentDepth%2 == 0:
                    if childUtility > alpha:
                        evaluationUtility = childUtility

                        if childUtility < beta:
                            alpha = childUtility
                        else:
                            isBreak = True
                            break
                else:
                    if childUtility < beta:
                        evaluationUtility = childUtility

                        if childUtility > alpha:
                            beta = childUtility
                        else:
                            isBreak = True
                            break

                if currentDepth != 0:
                    printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile)
                else:
                    printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile)

    if isBreak == True:
        if currentDepth  != 0:
            printABLog(getBoardPosition(iSelfPosition,jSelfPosition),currentDepth,evaluationUtility,alpha,beta,traverseLogFile)
        else:
            printABLog('root',currentDepth,evaluationUtility,alpha,beta,traverseLogFile)


    return evaluationUtility

#----------------------------------------Input and Control--------------------------------------------------


#1.Handling the Input

#Initialisation of the variables
gameTask = 0
gamePlayer = 0
gameEnemyPlayer = 0
gameCutOff = 0

boardValues = []
boardState = []

#Reading the input file
inputFile = open('input.txt')

#Reading the game task player and cutoff
gameTask  = inputFile.readline().strip()
gameTask = int(gameTask)
gamePlayer = inputFile.readline().strip()
gameCutOff = inputFile.readline().strip()
gameCutOff = int(gameCutOff)
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

#2.Control

if gameTask == 1:
    print 'Greedy Best First Search in execution.'
    GBFS(gameTask,gamePlayer,gameEnemyPlayer,gameCutOff,boardValues,boardState)
elif gameTask == 2:
    print 'Minimax Search in execution.'
    traverseLogFile = open('traverse_log.txt','w')
    traverseLogFile.write("Node,Depth,Value\n")
    result = MINIMAX(boardState,boardValues,gamePlayer,gamePlayer,gameCutOff,0,-99,-99,traverseLogFile)
    traverseLogFile.close()

    print 'Final Utility Value:',result
elif gameTask == 3:
    print 'Alpha-Beta Pruning Search in execution.'
    traverseLogFile = open('traverse_log.txt','w')
    traverseLogFile.write("Node,Depth,Value,Alpha,Beta\n")
    result = ABPrune(boardState,boardValues,gamePlayer,gamePlayer,gameCutOff,0,-99,-99,-float('inf'),float('inf'),traverseLogFile)
    traverseLogFile.close()

    print 'Final Utility Value:',result#,', alpha:',alpha,', beta:',beta




