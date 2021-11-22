import pygame
import numpy as np
import random

screen = pygame.display.set_mode((600, 700))
game_over = False
radius = 45

pygame.display.set_caption("Connect Four")
screen.fill((255, 255, 255))
# image = pygame.image.load("red-circle-1155276042606ekqvli9k.png")
# pygame.mouse.set_visible(False)
# pygame.mouse.set_cursor(image)


def create_board():
    board = np.zeros((6, 7))  # matrix of zeros 6 x 7
    return board


def is_valid_location(board, col):
    return board[5][col] == 0


def draw_board(board):
    for i in range(6):
        for j in range(7):
            pygame.draw.rect(screen, (0, 0, 255), (i * 100, j * 100 + 100, 100, 100))
            pygame.draw.circle(screen, (18, 25, 64), ((i * 100 + 100 / 2), j * 100 + 100 + 100 / 2), radius)
    for i in range(6):
        for j in range(7):
            if board[i][j] == 1:
                pygame.draw.circle(screen, (255, 0, 0), ((i * 100 + 100 / 2), 700 - j * 100 + 100 + 100 / 2), radius)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, (255, 255, 0), ((i * 100 + 100 / 2), 700 - j * 100 + 100 + 100 / 2), radius)

    pygame.display.update()


turn = random.randint(0, 1)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    board = create_board()
    draw_board(board)