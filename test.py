board = ["0000002", "0000020", "0010200", "0002000", "0020100", "0200100"]


def getscore(board):
    maxscore = getmaxscore(board)
    print(maxscore)
    minscore = getminscore(board)
    print(minscore)
    return maxscore, minscore


def getmaxscore(board):
    score = 0
    score += checkcolumn(board, "1")
    score += checkdiagonal(board, "1")
    for i in range(0, 6):
        score += checkrow(board[i], "1")
    return score


def getminscore(board):
    score = 0
    score += checkcolumn(board, "2")
    score += checkdiagonal(board, "2")
    for i in range(0, 6):
        score += checkrow(board[i], "2")
    return score


# def play(turn, board):
#     if turn == 1:
        # max plays
        # generatepossbilemoves(board)


def generatepossbilemoves(current):
    possiblemoves = []
    for i in range(0, 6):
        indices = getpos(current[i])
        for j in indices:
            print("row", i, "column", j)



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
        else:
            connection = 0
        if connection >= 4:
            score += 1
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
    while row < 6 and column < 7:
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
getscore(board)