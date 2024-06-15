import pygame
from pygame.locals import *
import board_gui as gui

# Colors
GREEN = (50, 70, 50)

def pvp(mySurface, n):
    currentPlayer = 1
    scores = [0, 0]
    board = [[0] * n for _ in range(n)]
    mySurface.fill(GREEN)
    gui.drawBoard(mySurface, n)
    gui.displayTeam(mySurface)
    gui.displayPlayer(mySurface, 1)
    gui.displayScore(mySurface, scores)
    while True:
        gameFinished = True
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    gameFinished = False
        if gameFinished:
            break
        events = pygame.event.get()
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if (70 < x < 70 + 70 * n) and (70 < y < 70 + 70 * n):
                    j = (x - 70) // 70
                    i = (y - 70) // 70
                    if board[i][j] == 0:
                        board[i][j] = currentPlayer
                        gui.drawCell(mySurface, board, i, j, currentPlayer)
                        lines = checkForSOS(board, i, j)
                        if lines:
                            scores[currentPlayer - 1] += len(lines)
                            gui.displayScore(mySurface, scores)
                            gui.drawLines(mySurface, lines, currentPlayer)
                        currentPlayer = 3 - currentPlayer  # Toggle player
                        gui.displayPlayer(mySurface, currentPlayer)
            if event.type == QUIT:
                return

def checkForSOS(board, row, col):
    n = len(board)
    lines = []

    # Horizontal SOS
    if col - 2 >= 0 and board[row][col] == 'S' and board[row][col - 1] == 'O' and board[row][col - 2] == 'S':
        lines.append((row, col - 2, row, col))
    if col + 2 < n and board[row][col] == 'S' and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
        lines.append((row, col, row, col + 2))
    if col - 1 >= 0 and col + 1 < n and board[row][col - 1] == 'S' and board[row][col] == 'O' and board[row][col + 1] == 'S':
        lines.append((row, col - 1, row, col + 1))

    # Vertical SOS
    if row - 2 >= 0 and board[row][col] == 'S' and board[row - 1][col] == 'O' and board[row - 2][col] == 'S':
        lines.append((row - 2, col, row, col))
    if row + 2 < n and board[row][col] == 'S' and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
        lines.append((row, col, row + 2, col))
    if row - 1 >= 0 and row + 1 < n and board[row - 1][col] == 'S' and board[row][col] == 'O' and board[row + 1][col] == 'S':
        lines.append((row - 1, col, row + 1, col))

    # Diagonal SOS
    if row - 2 >= 0 and col - 2 >= 0 and board[row][col] == 'S' and board[row - 1][col - 1] == 'O' and board[row - 2][col - 2] == 'S':
        lines.append((row - 2, col - 2, row, col))
    if row + 2 < n and col + 2 < n and board[row][col] == 'S' and board[row + 1][col + 1] == 'O' and board[row + 2][col + 2] == 'S':
        lines.append((row, col, row + 2, col + 2))
    if row - 2 >= 0 and col + 2 < n and board[row][col] == 'S' and board[row - 1][col + 1] == 'O' and board[row - 2][col + 2] == 'S':
        lines.append((row - 2, col + 2, row, col))
    if row + 2 < n and col - 2 >= 0 and board[row][col] == 'S' and board[row + 1][col - 1] == 'O' and board[row + 2][col - 2] == 'S':
        lines.append((row, col, row + 2, col - 2))

    return lines
