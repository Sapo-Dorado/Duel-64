import pygame
import sys
from UI.constants import *
from UI.game_board import GameBoardUI

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

ui = GameBoardUI(screen)
while True:
    ui.update()
    clock.tick(60)

pygame.quit()
