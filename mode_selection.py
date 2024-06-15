import pygame
from pygame.locals import *
from main import gameloop

# Colors
GREY = (70, 70, 70)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
YELLOW = (255, 100, 0)

# Resolution
heigth = 600
width = 900

# Fonts and Text
pygame.init()
logoFont = pygame.font.Font('font/solid.ttf', 100)
sbuttonFont = pygame.font.Font('font/solid.ttf', 50)
mbuttonFont = pygame.font.Font('font/solid.ttf', 20)

logoText = logoFont.render('S O S', True, BLACK)
sbuttonText = sbuttonFont.render('SOLO', True, BLACK)
sbuttonhoverText = sbuttonFont.render('SOLO', True, ORANGE)
mbuttonText = mbuttonFont.render('MULTIPLAYER', True, BLACK)
mbuttonhoverText = mbuttonFont.render('MULTIPLAYER', True, ORANGE)

def menu():
    pygame.init()
    mySurface = pygame.display.set_mode((width, heigth))
    pygame.display.set_caption('SOS')
    inProgress = True

    # Define tableSize and squareSize here
    tableSize = 6
    squareSize = 70

    mySurface.fill(GREY)
    displayLogo(mySurface)
    while inProgress:
        drawButton(mySurface, BLACK, 0)
        mouse = pygame.mouse.get_pos()
        if (380 + 150 > mouse[0] > 380 and 240 + 50 > mouse[1] > 240):
            drawButton(mySurface, YELLOW, 1)
        elif (380 + 150 > mouse[0] > 380 and 310 + 50 > mouse[1] > 310):
            drawButton(mySurface, YELLOW, 2)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if (380 + 150 > mouse[0] > 380 and 240 + 50 > mouse[1] > 240):
                    gameloop(tableSize, squareSize, 'solo')
                    inProgress = False
                if (380 + 150 > mouse[0] > 380 and 310 + 50 > mouse[1] > 310):
                    gameloop(tableSize, squareSize, 'multiplayer')
                    inProgress = False
            if event.type == QUIT:
                inProgress = False
        if inProgress:
            pygame.display.update()
    pygame.quit()

def displayLogo(mySurface):
    textRect = logoText.get_rect()
    textRect.topleft = (320, 110)
    mySurface.blit(logoText, textRect)

def drawButton(mySurface, textColor, option):
    pygame.draw.rect(mySurface, WHITE, (380, 240, 150, 50))
    pygame.draw.rect(mySurface, WHITE, (380, 310, 150, 50))
    textRect = sbuttonText.get_rect()
    textRect.topleft = (386, 249)
    if option == 1:
        mySurface.blit(sbuttonhoverText, textRect)
    else:
        mySurface.blit(sbuttonText, textRect)
    textRect = mbuttonText.get_rect()
    textRect.topleft = (383, 328)
    if option == 2:
        mySurface.blit(mbuttonhoverText, textRect)
    else:
        mySurface.blit(mbuttonText, textRect)
