import pygame
import mode_selection
import two_player_logic
import single_player_logic

# Resolution
height = 600
width = 900

# Table and square sizes
tableSize = 6
squareSize = 70

def gameloop(tableSize, squareSize, mode):
    pygame.init()
    mySurface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SOS')

    if mode == 'solo':
        single_player_logic.pve(mySurface, tableSize)
    else:
        two_player_logic.pvp(mySurface, tableSize)

if __name__ == '__main__':
    mode_selection.menu()
