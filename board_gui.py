import pygame
from pygame.locals import *

# Colors
GREY = (70, 70, 70)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
GREEN = (50, 70, 50)

# Fonts
pygame.init()
boardFont = pygame.font.Font('font/Washington.ttf', 45)
scoreFont = pygame.font.Font('font/Washington.ttf', 48)
score1Font = pygame.font.Font('font/Digit.TTF', 48)
playerFont = pygame.font.Font('font/Washington.ttf', 48)
cellFont = pygame.font.Font('font/Washington.ttf', 55)

# Text
boardText = boardFont.render('S | O', True, ORANGE)
bscoreText = scoreFont.render('Blue:', True, BLUE)
rscoreText = scoreFont.render('Red:', True, RED)
player1onText = playerFont.render('<--', True, BLUE)
player2onText = playerFont.render('<--', True, RED)
playeroffText = playerFont.render('<--', True, GREY)

def drawBoard(mySurface, n):
    x = 70
    y = 70
    size = 70
    for i in range(n):
        for j in range(n):
            drawBoardCell(mySurface, WHITE, x, y, size)    
            x += size
        x = 70
        y += size

def drawBoardCell(mySurface, COLOR, x, y, size):
    pos1 = (x, y)
    pos2 = (x + size, y)
    pos3 = (x + size, y + size)
    pos4 = (x, y + size)
    pygame.draw.line(mySurface, COLOR, pos1, pos2)
    pygame.draw.line(mySurface, COLOR, pos2, pos3)
    pygame.draw.line(mySurface, COLOR, pos3, pos4)
    pygame.draw.line(mySurface, COLOR, pos4, pos1)
    drawBoardLetter(mySurface, x, y, size)

def drawBoardLetter(mySurface, x, y, size):
    textRect = boardText.get_rect()
    textRect.topleft = (x, y + 15)
    mySurface.blit(boardText, textRect)

def displayTeam(mySurface):
    textRect = bscoreText.get_rect()
    textRect.topleft = (600, 200)
    mySurface.blit(bscoreText, textRect)
    textRect.topleft = (600, 300)
    mySurface.blit(rscoreText, textRect)

def displayScore(mySurface, scores):
    clearScore(mySurface)
    player1str = str(scores[0])
    player2str = str(scores[1])
    player1 = score1Font.render(player1str, True, WHITE)
    player2 = score1Font.render(player2str, True, WHITE)
    textRect = player1.get_rect()
    textRect.topleft = (715, 190)
    mySurface.blit(player1, textRect)
    textRect.topleft = (715, 290)
    mySurface.blit(player2, textRect)

def clearScore(mySurface):
    rect = (715, 190, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)
    rect = (715, 290, 70, 70)
    pygame.draw.rect(mySurface, GREY, rect)

def displayPlayer(mySurface, player):
    if player == 1:
        textRect = player1onText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(player1onText, textRect)
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(playeroffText, textRect)
    elif player == 2:
        textRect = playeroffText.get_rect()
        textRect.topleft = (800, 200)
        mySurface.blit(playeroffText, textRect)
        textRect = player2onText.get_rect()
        textRect.topleft = (800, 300)
        mySurface.blit(player2onText, textRect)

def drawCell(mySurface, board, i, j, player):
    letter = 'S' if board[i][j] == 1 else 'O'
    clearCell(mySurface, board, i, j)
    x = 71 + (j * 70) + 18
    y = 71 + (i * 70) + 12
    text = cellFont.render(letter, True, BLUE if player == 1 else RED)
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    mySurface.blit(text, textRect)

def clearCell(mySurface, board, i, j):
    x = 71 + (j * 70)
    y = 71 + (i * 70)
    rect = (x, y, 69, 69)
    pygame.draw.rect(mySurface, GREEN, rect)

def drawLines(mySurface, lines, player):
    if lines:
        for line in lines:
            if line[1] == line[3]:
                x = 70 * (line[1] + 1) + 35 
                y = 70 * (line[0] + 1) + 15
                x1 = 70 * (line[3] + 1) + 35
                y1 = 70 * (line[2] + 1) + 120
            elif line[0] == line[2]:
                x = 70 * (line[1] + 1) + 20
                y = 70 * (line[0] + 1) + 35
                x1 = 70 * (line[3] + 1) + 120
                y1 = 70 * (line[2] + 1) + 35
            elif (line[2] - line[0]) == (line[3] - line[1]):
                x = 70 * (line[1] + 1) + 20
                y = 70 * (line[0] + 1) + 20
                x1 = 70 * (line[3] + 1) + 120
                y1 = 70 * (line[2] + 1) + 120
            elif (line[2] - line[0]) == - (line[3] - line[1]):
                x = 70 * (line[1] + 1) + 20
                y = 70 * (line[0] + 1) + 120
                x1 = 70 * (line[3] + 1) + 120
                y1 = 70 * (line[2] + 1) + 20
            pygame.draw.line(mySurface, BLUE if player == 1 else RED, (x, y), (x1, y1), 2)
