#!/usr/bin/python3
import pygame
from pygame.locals import *
from sosINIT import *
from board_gui import gameloop

def menu():
    pygame.init()
    mySurface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SOS')
    inProgress = True

    mySurface.fill(GREY)
    displayLogo(mySurface)
    while inProgress:
        drawButton(mySurface, BLACK, 0)
        mouse = pygame.mouse.get_pos()
        if ((380 + 150) > mouse[0] > 380 and (240 + 50) > mouse[1] > 240):
            drawButton(mySurface, YELLOW, 1)
        elif ((380 + 150) > mouse[0] > 380 and (310 + 50) > mouse[1] > 310):
            drawButton(mySurface, YELLOW, 2)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if ((380 + 150) > mouse[0] > 380 and (240 + 50) > mouse[1] > 240):
                    gameloop(tableSize, squareSize)
                    inProgress = False
                if ((380 + 150) > mouse[0] > 380 and (310 + 50) > mouse[1] > 310):
                    gameloop(tableSize, squareSize)
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
