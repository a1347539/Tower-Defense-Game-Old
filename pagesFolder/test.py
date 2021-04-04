import pygame
from pages import *
import os



upgrade_img = pygame.image.load(os.path.join("img/tower_menu","upgrade.png"))

pygame.init()

width = 500
height = 500

screen = pygame.display.set_mode((width, height))

def drawMainPage(width,height):

    
    surfaces = ((0,0,width,40,upgrade_img),(0,40,60,height-40,upgrade_img),(60,40,width-60,height-40,upgrade_img))
    gameplay_page = page(width, height, surfaces, screen)
    gameplay_page.draw()
    
    

run = True

while run:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    drawMainPage(width,height)

    pygame.display.flip()

pygame.quit()
