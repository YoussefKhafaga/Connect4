board = ["0000000", "0111100", "0110110", "0001000", "0001000", "0001000"]


def calculateconnections(board, value, notvalue, numberofconnections):
    connection = 0
    score = 0
    bonus = blocked = 0
    # for Rows
    flag = 1
    for i in range(0, 6):
        tempbonus = 0
        flag = 1
        for j in range(0, 7):
            # print(connection)
            if board[i][j] == value:
                connection += 1
                if j == 3:
                    tempbonus += 0.4
                    if i == 2:
                        tempbonus += 0.4
                elif j == 2 or 1 or 4 or 5:
                    tempbonus += 0.2
                if connection == numberofconnections:
                    score += 1
                    connection = 0


def calculateconnections(board, value, notvalue, numberofconnections):
    connection = 0
    score = 0
    bonus = blocked = 0
    # for Rows
    flag = 1
    for i in range(0, 6):
        tempbonus = 0
        flag = 1
        for j in range(0, 7):
            # print(connection)
            if board[i][j] == value:
                connection += 1
                if j == 3:
                    tempbonus += 0.4
                    if i == 2:
                        tempbonus += 0.4
                elif j == 2 or 1 or 4 or 5:
                    tempbonus += 0.2
                if connection == numberofconnections:
                    score += 1
                    connection = 0
            elif board[i][j] == notvalue:
                if connection < 4:
                    if connection >= 1:
                        blocked += 1
                    flag = 0
                connection = 0
            else:
                connection = 0

        if flag:
            bonus += tempbonus

    connection = 0
    # for columns
    for i in range(0, 7):
        tempbonus = 0
        flag = 1
        for j in range(0, 6):
            # print(connection)
            if board[j][i] == value:
                connection += 1
                if i == 3:
                    tempbonus += 0.3
                    if j == 2:
                        tempbonus += 0.3
                elif i == 2 or 1 or 4 or 5:
                    tempbonus += 0.2
                if connection == numberofconnections:
                    score += 1
                    connection = 0
            elif board[j][i] == notvalue:
                if connection < 4:
                    if connection >= 1:
                        blocked += 1
                    flag = 0
                connection = 0
            else:
                connection = 0

        if flag:
            bonus += tempbonus
        connection = 0

    # for digaonal
    for i in range(0, 6):
        tempbonus = 0
        flag = 1
        for j in range(0, 7):
            row = i
            column = j
            while row < 6 and column < 7:
                if board[row][column] == value:
                    connection += 1
                    if row == 2:
                        tempbonus += 0.4
                        if column == 3:
                            tempbonus += 0.4
                    elif i == 2 or 1 or 4 or 5:
                        tempbonus += 0.2
                    if connection == numberofconnections:
                        score += 1
                        connection = 0
                elif board[row][column] == notvalue:
                    if connection < 4:
                        if connection >= 1:
                            blocked += 1
                        flag = 0
                    connection = 0
                else:
                    connection = 0
                row += 1
                column += 1
        if flag:
            bonus += tempbonus
        connection = 0

    # for reversed digaonal
    for i in range(0, 6):
        tempbonus = 0
        flag = 1
        for j in range(0, 7):
            row = i
            column = j
            while row < 6 and column < 7 and column > 0:
                if board[row][column] == value:
                    connection += 1
                    if row == 2:
                        tempbonus += 0.4
                        if column == 3:
                            tempbonus += 0.4
                    elif i == 2 or 1 or 4 or 5:
                        tempbonus += 0.2
                    if connection == numberofconnections:
                        score += 1
                        connection = 0
                elif board[row][column] == notvalue:
                    if connection < 4:
                        if connection >= 1:
                            blocked += 1
                        flag = 0
                    connection = 0
                else:
                    connection = 0
                row += 1
                column -= 1
        if flag:
            bonus += tempbonus
        connection = 0

    return score, bonus, blocked


def evaluation(board):
    value = "1"
    notvalue = "2"
    score = 0
    print("Twos", calculateconnections(board, value, notvalue, 2))
    print("Threes", calculateconnections(board, value, notvalue, 3))
    print("Fours", calculateconnections(board, value, notvalue, 4))
    x, y, z = calculateconnections(board, value, notvalue, 2)
    score += x * 10 + y * 10 - z * 10
    x, y, z = calculateconnections(board, value, notvalue, 3)
    score += x * 100 + y * 100 - z * 100
    x, y, z = calculateconnections(board, value, notvalue, 4)
    score += x * 1000 + y * 100 - z * 1000

    return score


if __name__ == '_main_':
    board = ["0111000", "0111100", "0110110", "0001000", "0001000", "0001000"]

    score = evaluation(board)
    print(score)