import time

board = ["1111111", "1111111", "1111111", "1111111", "1111111", "1111111"]
nextmoves = set()

def getscore(board):
    maxscore = getmaxscore(board)
    minscore = getminscore(board)
    return maxscore, minscore


def getmaxscore(board):
    score = 0
    for i in range(0, 6):
        score += checkrow(board[i], "1")
    score += checkcolumn(board, "1")
    score += checkdiagonal(board, "1")
    return score


def getminscore(board):
    score = 0
    for i in range(0, 6):
        score += checkrow(board[i], "2")
    score += checkcolumn(board, "2")
    score += checkdiagonal(board, "2")
    return score


def play(turn, board):
    if turn == 1:
        # max plays
        generatepossbilemoves(board)


def generatepossbilemoves(currentboardstate):
    possiblemoves = []
    # nextmoves = set()
    for i in range(0, 5):
        if currentboardstate[i] in nextmoves:
            return
    for i in range(0, 6):
        for j in range(0, 7):
            temp = currentboardstate.copy()
            if currentboardstate[i][j] == "1":
                # check column move
                if i < 5:
                    if currentboardstate[i+1][j] == "0":
                        temp2 = list(currentboardstate[i+1])
                        temp2[j] = "1"
                        string = ''.join(temp2)
                        temp[i+1] = string
                        # nextmoves.add(temp)
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row move
                if j != 6:
                    if currentboardstate[i][j+1] == "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j+1] = "1"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row reversed
                if j != 6 and j != 0:
                    if currentboardstate[i][j-1] == "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j-1] = "1"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
    return possiblemoves



def getpos(current, value):
    indices = []
    for i in range(0, len(current)):
        if current[i] == value:
            indices.append(i)
    return indices


def checkrow(board, value):
    score = 0
    connection = 0
    for i in board:
        if i == value:
            connection += 1
            if connection >= 4:
                score += 1
        else:
            connection = 0
    return score


def checkcolumn(board, value):
    connection = 0
    score = 0
    for i in range(0, 7):
        for j in range(0, 6):
            if board[j][i] == value:
                connection += 1
                if connection >= 4:
                    score += 1
            else:
                connection = 0
        connection = 0
    return score


def checkdiagonal(board, value):
    score = 0
    for i in range(0, 6):
        for j in range(0, 7):
            score += getdiagonalscore(i, j, board, value)
            score += getreversediagonalscore(i, j, board, value)
    return score

def getdiagonalscore(row, column, board, value):
    score = 0
    connection = 0
    while row < 6 and column < 7:
        if board[row][column] == value:
            connection += 1
            if connection == 4:
                score += 1
        else:
            connection = 0
        row += 1
        column += 1
    return score


def getreversediagonalscore(row, column, board, value):
    score = 0
    connection = 0
    while row < 6 and column < 7 and column >= 0:
        if board[row][column] == value:
            connection += 1
            if connection == 4:
                score += 1
        else:
            connection = 0
        row += 1
        column -= 1
    return score

# play(1, board)
print(getscore(board))
# generatepossbilemoves(board)
print(generatepossbilemoves(board))