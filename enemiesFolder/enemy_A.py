import pygame
import os
from .enemies import enemy
import random

enemy_imgs = []

direction = ["down","left","right","top"]

pic_temp = []

width = 15
height = 15

for d in direction:
    pic_temp.clear()
    for num in range(2):                    #numer of pic in one direction
        num = str(num)

        pic_temp.append(pygame.transform.scale(
        pygame.image.load(os.path.join(
            "img/enemy_img/"+d,"enemy"+num+".png")),(width,height)))

    
    enemy_imgs.append(pic_temp)
    
    pic_temp = []

class Enemy_A(enemy):

    def __init__(self, current_path, current_map, tileWidth, tileHeight):
        
        super().__init__(current_path, current_map, tileWidth, tileHeight)
        self.width = width
        self.height = height
        self.x = current_path[0][0]*tileWidth + random.randint(int(((tileWidth-self.width)/2)-6), int(((tileWidth-self.width)/2)+6))
        self.y = current_path[0][1]*tileHeight + random.randint(int(((tileHeight-self.width)/2)-6), int(((tileHeight-self.width)/2)+6))


        self.ds = 3                            #rate of speed, less = slower

        self.max_health = self.current_health = 33            #health


        self.enemy_imgs = enemy_imgs

        self.loot = 5        

