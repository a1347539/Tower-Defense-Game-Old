import pygame
import os
import math
from .towers import tower

width = 20
height = 25

supportTower_A_imgs = []
supportTower_B_imgs = []

supportTower_A_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("img/tower_img/support_tower","support_tower_A.png")),(width, height)))

locked_img = pygame.image.load(os.path.join(
    "img/tower_img/support_tower/","support_tower_A_locked.png"))


#increase range
class supportTower_A(tower):
    def __init__(self):
        super().__init__()
        self.id = 2
        self.type = "support"
        self.width = width                                  #tower config
        self.height = height

        self.general_upgrade = None
        self.tower_upgrade = None
        
        self.effect = [1.1,1.6]
        self.sell_price = [1,3,5]
        self.upgrade_price = [1,2,3]

        self.tower_in_range = []

        if self.general_upgrade != None:
            upgrade_range = self.general_upgrade["range"][0]*0.4 + self.tower_upgrade["range"][0]*0.6
        else:
            upgrade_range = 0
        
        self.radius = 100 + upgrade_range
        
        self.tower_imgs = supportTower_A_imgs
        self.locked_img = locked_img
        
        self.distance_fromEnemy = None

        self.isAttack = False

        self.atk_tower_radius = None
        

    def draw(self, screen):
        super().draw(screen)
        
    def support(self, towers):
        
        in_range = []
        
        for tower in towers:
            
            distance_fromTower = math.sqrt((self.x - tower.x)**2 + (self.y - tower.y)**2)
            
            if distance_fromTower + 3 < self.radius and tower not in self.tower_in_range:
                #need sorting maybe
                self.tower_in_range.append(tower)
                
        for tower in self.tower_in_range:
            if tower.atk_tower_radius != None:
                tower.radius = int(tower.atk_tower_radius * self.effect[self.level]) + self.general_upgrade["effect"][0]*0.1 + self.tower_upgrade["effect"][0]*0.3

                distance_fromTower = math.sqrt((self.x - tower.x)**2 + (self.y - tower.y)**2)
                if distance_fromTower > self.radius and tower in self.tower_in_range:
                    self.tower_in_range.remove(tower)
                    
                

class supportTower_B(tower):
    def __init__(self):
        super().__init__()
    
        self.width = width                                  #tower config
        self.height = height

        self.effect = [1,3,1.9]
        self.level = 0
        self.tower_in_range = []
        
        
        self.radius = 100
        self.tower_imgs = supportTower_B_imgs


    def draw(self, screen):
        super().draw_radius(screen)
        super().draw(screen)
        
    def support(self, towers):
        
        in_range = []
        
        for tower in towers:
            
            distance_fromTower = math.sqrt((self.x - tower.x)**2 + (self.y - tower.y)**2)
            
            if distance_fromTower + 3 < self.radius and tower not in self.tower_in_range:
                #need sorting maybe
                self.tower_in_range.append(tower)
                
        for tower in self.tower_in_range:
            tower.damage = int(tower.current_damage * self.effect[self.level])

            distance_fromTower = math.sqrt((self.x - tower.x)**2 + (self.y - tower.y)**2)
            if distance_fromTower > self.radius and tower in self.tower_in_range:
                self.tower_in_range.remove(tower)
                
                

    def attack(self):
        pass

















