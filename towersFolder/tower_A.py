import pygame
import os
import math

from .towers import tower

tower_imgs = []
projectile_imgs = []

width = 33
height = 37

projectile_width = 3
projectile_height = 5


for num in range(3):
    tower_imgs.append(pygame.transform.scale(
    pygame.image.load(os.path.join(
        "img/tower_img/tower_A/","tower_A_"+str(num)+".png")),(width, height)))

projectile_imgs.append(pygame.transform.scale(
    pygame.image.load(os.path.join(
        "img/tower_img/tower_A/","projectile_A_1.png")),(projectile_width, projectile_height)))

locked_img = pygame.image.load(os.path.join(
    "img/tower_img/tower_A/","tower_A_locked.png"))


class Tower_A(tower):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.type = "attack"
        self.width = width                                  #tower config
        self.height = height
        
        self.general_upgrade = None
        self.tower_upgrade = None
        
        self.damage = [1,20,30]
        self.sell_price = [1,3,5]
        self.upgrade_price = [1,2,3]
        if self.general_upgrade != None:
            upgrade_atk = self.general_upgrade["attack_speed"][0]*0.1 + self.tower_upgrade["attack_speed"][0]*0.2
            upgrade_range = self.general_upgrade["range"][0]*0.2 + self.tower_upgrade["range"][0]*0.4
        else:
            upgrade_atk = 0
            upgrade_range = 0
        self.attack_speed = 1 + upgrade_atk
        self.radius = 70 + upgrade_range
        self.atk_tower_radius = self.radius

        self.tower_imgs = tower_imgs
        self.locked_img = locked_img

        self.projectile_imgs = projectile_imgs              #projectile config
        self.projectile_velocity = 5
        self.projectile_type = 1
        self.projectile_width = projectile_width
        self.projectile_height = projectile_height

    def draw(self, screen):
        super().draw(screen)
            

                
                


    


            
