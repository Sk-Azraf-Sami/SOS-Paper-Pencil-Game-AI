import pygame
from pygame.locals import *
import random
import board_gui as gui

# Colors
GREEN = (50, 70, 50)

def pve(mySurface, n):
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
        if currentPlayer == 1:
            events = pygame.event.get()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (70 < x < 70 + 70 * n) and (70 < y < 70 + 70 * n):
                        j = (x - 70) // 70
                        i = (y - 70) // 70
                        if board[i][j] == 0:
                            board[i][j] = 1 if event.button == 1 else 2
                            score, lines = calculateScore(board, n, i, j)
                            scores[currentPlayer - 1] += score
                            gui.drawCell(mySurface, board, i, j, currentPlayer)
                            gui.displayScore(mySurface, scores)
                            gui.drawLines(mySurface, lines, currentPlayer)
                            if score == 0:
                                currentPlayer = 2
                            gui.displayPlayer(mySurface, currentPlayer)
        else:
            i, j, value = computerMove(board, n)
            board[i][j] = value
            score, lines = calculateScore(board, n, i, j)
            scores[currentPlayer - 1] += score
            gui.drawCell(mySurface, board, i, j, currentPlayer)
            gui.displayScore(mySurface, scores)
            gui.drawLines(mySurface, lines, currentPlayer)
            if score == 0:
                currentPlayer = 1
            gui.displayPlayer(mySurface, currentPlayer)
        pygame.display.update()
    pygame.quit()

def calculateScore(board, n, row, col):
    totalScore = 0
    lines = []
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if drow == 0 and dcol == 0:
                continue
            s = countS(board, n, row, col, drow, dcol)
            if s == 3:
                totalScore += 1
                lines.append((row, col, row + 2 * drow, col + 2 * dcol))
    return totalScore, lines

def countS(board, n, row, col, drow, dcol):
    s = 0
    for k in range(3):
        r = row + k * drow
        c = col + k * dcol
        if 0 <= r < n and 0 <= c < n:
            s += 1 if board[r][c] == 1 else 2 if board[r][c] == 2 else 0
        else:
            return 0
    return s

def computerMove(board, n):
    emptyCells = [(i, j) for i in range(n) for j in range(n) if board[i][j] == 0]
    i, j = random.choice(emptyCells)
    value = random.choice([1, 2])
    return i, j, value
