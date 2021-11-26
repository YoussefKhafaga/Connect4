import time

board = ["0000100", "0000000", "0000000", "0000000", "0000000", "0000000"]
nextmoves = set()
plays = 0

def getscore(board):
    maxscore = getmaxscore(board)
    minscore = getminscore(board)
    return maxscore, minscore


def getmaxscore(board):
    score = 0
    for i in range(0, 6):
        score += checkrow(board[i], "1")
    if score == 0:
        return 0
    score += checkcolumn(board, "1")
    score += checkdiagonal(board, "1")
    return score


def getminscore(board):
    score = 0
    for i in range(0, 6):
        score += checkrow(board[i], "2")
    if score == 0:
        return 0
    score += checkcolumn(board, "2")
    score += checkdiagonal(board, "2")
    return score



def generatepossbilemoves(currentboardstate, plays):
    possiblemoves = []
    if plays == 0:
        for i in range(0, 1):
            for j in range(0, 7):
                temp = currentboardstate.copy()
                if currentboardstate[i][j] == "0":
                    temp2 = list(currentboardstate[i])
                    temp2[j] = "2"
                    string = ''.join(temp2)
                    temp[i] = string
                else:
                    temp2 = list(currentboardstate[i])
                    temp2[j] = "2"
                    string = ''.join(temp2)
                    temp[i+1] = string
                if temp not in possiblemoves:
                    possiblemoves.append(temp)
                temp = currentboardstate.copy()
        plays += 1
    for i in range(0, 6):
        for j in range(0, 7):
            temp = currentboardstate.copy()
            if currentboardstate[i][j] == "2":
                # check column move
                if i < 5:
                    if currentboardstate[i+1][j] == "0":
                        temp2 = list(currentboardstate[i+1])
                        temp2[j] = "2"
                        string = ''.join(temp2)
                        temp[i+1] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row move
                if j != 6:
                    if currentboardstate[i][j+1] == "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j+1] = "2"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row reversed
                if j != 6 and j != 0:
                    if currentboardstate[i][j-1] == "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j-1] = "2"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
    return possiblemoves


def checkrow(board, value):
    score = 0
    connection = 0
    zeros = 0
    for i in board:
        if i == value:
            connection += 1
            if connection >= 4:
                score += 1
        else:
            zeros += 1
            if zeros == 7:
                return score
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
# print(getscore(board))
# generatepossbilemoves(board)
print(generatepossbilemoves(board, plays))