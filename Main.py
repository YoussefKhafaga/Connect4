import pygame
from pygame.locals import *
import numpy as np
import random
import math

import sys

pygame.init()

board1 = ["0000000", "0000000", "0000000", "0000000", "0000000", "0000000"]

font = pygame.font.SysFont('Constantia', 15)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
FONT = pygame.font.Font(None, 32)
COLOR_ACTIVE = pygame.Color('dodgerblue2')

screen = pygame.display.set_mode((700, 700))
radius = 45
rows = 6
columns = 7

pygame.display.set_caption("Connect Four")
screen.fill((255, 255, 255))
empty = 0
player_turn = 1
ai_turn = 2
plays = 0
minimax_tree = []


def create_board():
    board = np.zeros((rows, columns))  # matrix of zeros 6 x 7
    return board


def is_valid_location(board, col):
    return board[rows - 1][col] == 0


def game_end(board):
    for i in range(columns):
        for j in range(rows):
            if board[j][i] == 0:
                return False
    return True


def game_end1(board):
    for i in range(columns):
        for j in range(rows):
            if board[j][i] == "0":
                return False
    return True


def get_valid_locations(board):
    valid_locations = []
    for col in range(columns):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def next_valid_row(board, column):
    for r in range(rows):
        if board[r][column] == 0:
            return r


def drop_piece(board1, board, row, col, piece, spiece):
    board[row][col] = piece

    temp2 = list(board1[row])
    temp2[col] = spiece
    string = ''.join(temp2)
    board1[row] = string


def draw_board(board):
    for i in range(columns):
        for j in range(rows):
            pygame.draw.rect(screen, (0, 0, 255), (i * 100, j * 100 + 100, 100, 100))
            pygame.draw.circle(screen, (18, 25, 64), ((i * 100 + 100 / 2), (j * 100 + 100 + 100 / 2)), radius)
    for i in range(7):
        for j in range(6):
            if board[j][i] == 1:
                pygame.draw.circle(screen, (255, 0, 0), ((i * 100 + 100 / 2), 500 - j * 100 + 100 + 100 / 2), radius)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, (255, 255, 0), ((i * 100 + 100 / 2), 500 - j * 100 + 100 + 100 / 2), radius)

    pygame.display.update()


def print_board(board):
    for j in range(5, -1, -1):
        print(int(board[j][0]), '', int(board[j][1]), '', int(board[j][2]), '', int(board[j][3]),
              '',
              int(board[j][4]), '', int(board[j][5]), '', int(board[j][6]))


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
    for i in range(0, 6):
        for j in range(0, 7):
            temp = currentboardstate.copy()
            if currentboardstate[i][j] == "0" and (i == 0):
                temp2 = list(currentboardstate[i])
                temp2[j] = "2"
                string = ''.join(temp2)
                temp[i] = string
                if temp not in possiblemoves:
                    possiblemoves.append(temp)
                temp = currentboardstate.copy()
            if currentboardstate[i][j] == "2" or currentboardstate[i][j] == "1":
                # check column move
                if i < 5:
                    if currentboardstate[i + 1][j] == "0":
                        temp2 = list(currentboardstate[i + 1])
                        temp2[j] = "2"
                        string = ''.join(temp2)
                        temp[i + 1] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row move
                if j != 6:
                    if currentboardstate[i][j + 1] == "0" and currentboardstate[i - 1][j + 1] != "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j + 1] = "2"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
                # check row reversed
                if j != 6 and j != 0:
                    if currentboardstate[i][j - 1] == "0" and currentboardstate[i - 1][j - 1] != "0":
                        temp2 = list(currentboardstate[i])
                        temp2[j - 1] = "2"
                        string = ''.join(temp2)
                        temp[i] = string
                        if temp not in possiblemoves:
                            possiblemoves.append(temp)
                        temp = currentboardstate.copy()
    # print(possiblemoves)
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


def maximize(board, k):
    k = int(k)
    # if game_end1(board):
    #     return None, evaluation(board, "2", "1")
    if k == 0:
        return None, evaluation(board, "2", "1")
    k -= 1
    (max_child, max_utility) = (None, -math.inf)
    for move in generatepossbilemoves(board, plays):
        (temp, utility) = minimize(move, k)
        minimax_tree.append((utility, k))
        if utility > max_utility:
            (max_child, max_utility) = (move, utility)
    return max_child, max_utility


def minimize(board, k):
    k = int(k)
    if game_end1(board):
        return None, evaluation(board, "1", "2")
    if k == 0:
        return None, evaluation(board, "1", "2")
    k -= 1
    (min_child, min_utility) = (None, math.inf)
    for move in generatepossbilemoves(board, plays):
        temp, utility = maximize(move, k)
        minimax_tree.append((utility, k))
        if utility < min_utility:
            (min_child, min_utility) = (move, utility)
    return min_child, min_utility


def decision(board, k):
    child, utility = maximize(board, k)
    # print(child)
    return child


def maximize_pruning(board, alpha, beta, k):
    if game_end(board):
        return None, evaluation(board, "2", "1")
    if k == 0:
        return None, evaluation(board, "2", "1")
    k -= 1
    (max_child, max_utility) = (None, -math.inf)
    for move in generatepossbilemoves(board, plays):
        (temp, utility) = minimize_pruning(move, alpha, beta, k)
        if utility > max_utility:
            (max_child, max_utility) = (move, utility)
        if max_utility > alpha:
            max_utility = alpha
        if max_utility > beta:
            break
    return max_child, max_utility


def minimize_pruning(board, alpha, beta, k):
    if game_end(board):
        return (None, evaluation(board, "1", "2"))
    if k == 0:
        return None, evaluation(board, "1", "2")
    k -= 1
    (min_child, min_utility) = (None, math.inf)
    for move in generatepossbilemoves(board, plays):
        temp, utility = maximize_pruning(move, alpha, beta, k)
        if utility < min_utility:
            (min_child, min_utility) = (move, utility)
        if min_utility < alpha:
            break
        if min_utility < beta:
            beta = min_utility
    return min_child, min_utility


def decision_pruning(board, k):
    child, utility = maximize_pruning(board, -math.inf, math.inf, k)
    return child


def calculateconnections(board1, value, notvalue, numberofconnections):
    valueconnection = 0
    notvalueconnection = 0
    blocks = 0
    score = 0

    # for Rows
    for i in range(0, 6):
        for j in range(0, 7):

            # limit the connections (There is no need to check for them)
            if valueconnection == 0 and board1[i][j] == notvalue:
                if j == 5 and numberofconnections == 2:
                    break
                if j == 4 and numberofconnections == 3:
                    break
                if j == 3 and numberofconnections == 4:
                    break

            # giving a score for blocks with scale if it blocks more connection
            if board1[i][j] == value:
                valueconnection += 1
                # if we blocked 2 connections for player
                if notvalueconnection == 1:
                    blocks += 8
                # if we blocked 3 connection for player
                elif notvalueconnection == 2:
                    blocks += 27
                # if we blocked 4 connection for player
                elif notvalueconnection == 3:
                    blocks += 64
                # if we blocked more than 4 connection for player
                else:
                    blocks += 100
                notvalueconnection = 0

                if valueconnection == numberofconnections:
                    score += 1
                    valueconnection -= 1

            # if its a player chip increment player connections
            elif board1[i][j] == notvalue:
                notvalueconnection += 1
            # if empty place reset connections
            else:
                valueconnection = 0
                notvalueconnection = 0

    valueconnection = 0
    notvalueconnection = 0

    # for columns
    for i in range(0, 7):
        bonus = 0

        for j in range(0, 6):
            if valueconnection == 0 and board1[j][i] == notvalue:
                if j == 4 and numberofconnections == 2:
                    break
                if j == 3 and numberofconnections == 3:
                    break
                if j == 2 and numberofconnections == 4:
                    break

            if board1[j][i] == value:
                valueconnection += 1
                if i == 3:
                    score += 1
                    # if we blocked 2 connections for player
                    if notvalueconnection == 1:
                        blocks += 8
                    # if we blocked 3 connection for player
                    elif notvalueconnection == 2:
                        blocks += 27
                    # if we blocked 4 connection for player
                    elif notvalueconnection == 3:
                        blocks += 64
                    # if we blocked more than 4 connection for player
                    else:
                        blocks += 100
                notvalueconnection = 0

                if valueconnection == numberofconnections:
                    score += 1
                    valueconnection -= 1

            elif board1[j][i] == notvalue:
                notvalueconnection += 1
            else:
                notvalueconnection = 0
                valueconnection = 0
    notvalueconnection = 0
    valueconnection = 0

    # for digaonal
    for i in range(0, 6):
        for j in range(0, 7):
            row = i
            column = j
            while row < 6 and column < 7:
                if (column >= 4 and row <= 3) or (column <= 2 and row >= 3):
                    break

                if board1[row][column] == value:
                    valueconnection += 1
                    # if we blocked 2 connections for player
                    if notvalueconnection == 1:
                        blocks += 8
                    # if we blocked 3 connection for player
                    elif notvalueconnection == 2:
                        blocks += 27
                    # if we blocked 4 connection for player
                    elif notvalueconnection == 3:
                        blocks += 64
                    # if we blocked more than 4 connection for player
                    else:
                        blocks += 100
                    notvalueconnection = 0

                    if valueconnection == numberofconnections:
                        score += 1
                        valueconnection -= 1

                elif board1[row][column] == notvalue:
                    notvalueconnection += 1

                else:
                    notvalueconnection = 0
                    valueconnection = 0
                row += 1
                column += 1
        valueconnection = 0
        notvalueconnection = 0
    valueconnection = 0
    notvalueconnection = 0

    # for reversed digaonal
    for i in range(0, 6):
        for j in range(0, 7):
            row = i
            column = j
            while row < 6 and column < 7 and column > 0:
                if (column >= 4 and row >= 3 ) or (column <= 2 and row <= 3):
                    break

                if board1[row][column] == value:
                    valueconnection += 1
                    # if we blocked 2 connections for player
                    if notvalueconnection == 1:
                        blocks += 8
                    # if we blocked 3 connection for player
                    elif notvalueconnection == 2:
                        blocks += 27
                    # if we blocked 4 connection for player
                    elif notvalueconnection == 3:
                        blocks += 64
                    # if we blocked more than 4 connection for player
                    else:
                        blocks += 100
                    notvalueconnection = 0

                    if valueconnection == numberofconnections:
                        score += 1
                        break

                elif board1[row][column] == notvalue:
                    notvalueconnection += 1

                else:
                    notvalueconnection = 0
                    valueconnection = 0
                row += 1
                column -= 1
        notvalueconnection = 0
        valueconnection = 0

    return score + blocks

def evaluation(board, value, notvalue):
    score = 0
    score += calculateconnections(board, "2", "1", 2)
    score += calculateconnections(board, "2", "1", 3)
    score += calculateconnections(board, "2", "1", 4)
    return score


# define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# define global variable
clicked = False


class button():
    # colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 180
    height = 70

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main_menu():
    with_pruning = button(75, 200, 'with alpha-beta pruning')
    without_pruning = button(325, 200, 'without alpha-beta pruning')
    input_k_box = InputBox(200, 100, 140, 32)

    screen_width = 700
    screen_height = 700

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('main menu')
    while True:
        screen.fill(bg)
        with_pruning_var = True
        input_k_box.draw(screen)
        if with_pruning.draw_button():
            game(k, with_pruning_var)
            print('with pruning')
        if without_pruning.draw_button():
            with_pruning_var = False
            game(k, with_pruning_var)
            print('without pruning')

        for event in pygame.event.get():
            input_k_box.handle_event(event)
            if event.type == pygame.QUIT:
                run = False
        k = input_k_box.text
        pygame.display.update()


def game(k, with_pruning):
    # print(k, with_pruning)
    game_over = False
    turn = 1
    board = create_board()
    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, (255, 255, 255), (0, 0, 700, 100))
                posx = event.pos[0]
                if turn == player_turn:
                    pygame.draw.circle(screen, (255, 0, 0), (posx, 50), radius)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 700, 100))
                if turn == player_turn:
                    posx = event.pos[0]
                    col = int(math.floor(posx / 100))

                    if is_valid_location(board, col):
                        row = next_valid_row(board, col)
                        drop_piece(board1, board, row, col, 1, "1")
                        # print(board1)
                        draw_board(board)
                        print_board(board)
                        print("\n")
                        turn = 2
            if turn == ai_turn:
                # show minimax tree here.
                temp = k
                row = 0
                col = 0
                if with_pruning == True:
                    child = decision_pruning(board1, temp)
                else:
                    child = decision(board1, temp)
                print(child)
                for i in range(0, 6):
                    for j in range(0, 7):
                        if child[i][j] != board1[i][j]:
                            row = i
                            col = j
                            break
                    if row != col:
                        break
                pygame.time.wait(100)
                drop_piece(board1, board, row, col, 2, "2")
                # print(board1)
                draw_board(board)
                print_board(board)
                print("\n")
                turn = 1

            if game_end(board):
                pygame.time.wait(4000)
                game_over = True
    pygame.display.quit()
    pygame.quit()


main_menu()