import pygame
import sys
from UI.constants import *
from UI.game_board import GameBoardUI

# pygame setup
pygame.init()
global SCREEN, CLOCK
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()


def quitButton():
    # light shade of the button
    color_light = (170,170,170)
    
    # dark shade of the button
    color_dark = (100,100,100)
    
    # stores the width of the
    # screen into a variable
    width = screen.get_width()
    
    # stores the height of the
    # screen into a variable
    height = screen.get_height()
    
    # defining a font
    smallfont = pygame.font.SysFont('Corbel',35)

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    
    # rendering a text written in
    # this font
    text = smallfont.render('quit' , True , "white")
  
    for ev in pygame.event.get():
            
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
                
            #if the mouse is clicked on the
            # button the game is terminated
            if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
                pygame.quit()
        
        
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
        pygame.draw.rect(screen,color_light,[width-140,0,140,40])
            
    else:
        pygame.draw.rect(screen,color_dark,[width-140,0,140,40])
        
    # superimposing the text onto our button
    screen.blit(text , (width-100,0))
        
    # updates the frames of the game
    pygame.display.update()

def moveButton():
    global player_pos
    width = screen.get_width()
    # light shade of the button
    color_light = (170,170,170)
    
    # dark shade of the button
    color_dark = (100,100,100)
    
    # defining a font
    smallfont = pygame.font.SysFont('Corbel',35)
    
    # rendering a text written in
    # this font
    text = smallfont.render('move here' , True , "white")
  
    while True:
        
        for ev in pygame.event.get():
            
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                
                #if the mouse is clicked on the
                # button the game is terminated
                if player_pos[0]+45 <= mouse[0] <= player_pos[0]+45+90 and player_pos[1]-45 <= mouse[1] <= player_pos[1]+45:
                    player_pos = pygame.Vector2(player_pos[0]+90,player_pos[1])
                    drawGrid()
                    pygame.draw.circle(screen, "grey", player_pos, 40)
        
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        
        # if mouse is hovered on a button it
        # changes to lighter shade 
        if player_pos[0]+45 <= mouse[0] <= player_pos[0]+45+90 and player_pos[1]-45 <= mouse[1] <= player_pos[1]+45:
            pygame.draw.rect(screen,color_light,[player_pos[0]+45,player_pos[0]+45+90,80,80])
            
        else:
            pygame.draw.rect(screen,color_dark,[width-140,0,80,80])
        
        # superimposing the text onto our button
        screen.blit(text , (width-100,0))
        
        # updates the frames of the game
        pygame.display.update()




# player_pos = pygame.Vector2(45, 45)
# pygame.draw.circle(screen, "grey", player_pos, 40)
# moveButton()

ui = GameBoardUI(screen)
while True:
    ui.update()

pygame.quit()
