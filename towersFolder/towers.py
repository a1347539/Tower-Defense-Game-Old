import pygame
import os
from menuFolder.menu import menu
import time
import math
from .projectiles import proj

button_length = 17
#menu_bg = pygame.transform.scale(
#pygame.image.load(os.path.join(
#    "img","menu_bg.png")),(menu_width, menu_height))
upgrade_img = pygame.transform.scale(
    pygame.image.load(os.path.join(
        "img/tower_menu","upgrade.png")),(button_length, button_length))
sellTower_img = pygame.transform.scale(
    pygame.image.load(os.path.join(
        "img/tower_menu","sell_tower.png")),(button_length, button_length))



class tower:
    def __init__(self):
        self.xpos = None
        self.ypos = None
        self.x = None
        self.y = None
        self.level = 0
    
        self.selected = False
        self.isUpgrade = False
        self.menu_items = ((upgrade_img,"upgrade", None, None), (sellTower_img,"sell", None, None))
        self.menu = menu(None,None,
                         button_length*len(self.menu_items)+(len(self.menu_items)+1)*2, button_length, self.menu_items, None, None,
                         None, None, None,
                         button_length, button_length, 2,
                         None, None)

        self.targetEnemey = []
        self.projectiles = []
        
        self.attack_timer = time.time()

        self.isPaused = False

    def draw(self, screen):
        self.menu.ori_x = self.x - ((len(self.menu_items)*(button_length+2))-40)/2
        self.menu.ori_y = self.y-12
        screen.blit(self.tower_imgs[0],(self.x+1, self.y+1))  #index will change once have more images

        if self.selected is True:
            self.draw_radius(screen)
            self.menu.draw_horizontal_small(screen)
                    
    
            
    def draw_radius(self, screen):
        #draw range of tower
        circle_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (120,120,120, 100), (self.radius, self.radius), self.radius, 0)
        screen.blit(circle_surface, (self.x - self.radius + self.width/2 + 1,
                                     self.y - self.radius + self.height/2 + 1))

    def attack(self, screen, enemies):
        
        for enemy in enemies:
            self.distance_fromEnemy = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
            if self.distance_fromEnemy < self.radius and enemy not in self.targetEnemey:
                self.targetEnemey.append(enemy)             #need sorting maybe

        if len(self.targetEnemey) > 0:
            self.tageting = self.targetEnemey[0]
            
            distance_targetEnemy = math.sqrt((self.x - self.tageting.x)**2 + (self.y - self.tageting.y)**2)

            if self.tageting.isDead or distance_targetEnemy > self.radius:
                self.targetEnemey.remove(self.tageting)
            
            elif time.time() - self.attack_timer > 1/self.attack_speed:
                if not self.isPaused:
                    self.projectiles.append(proj(self, self.tageting,
                                                 self.projectile_imgs,
                                                 self.projectile_velocity,
                                                 self.projectile_type,
                                                 self.projectile_width,
                                                 self.projectile_height))
                    self.attack_timer = time.time()
                
        if self.projectiles:
            for projectile in self.projectiles:
                if self.isPaused:
                    projectile.Paused = 0
                else:
                    projectile.Paused = 1
                projectile.draw(screen)
                if projectile.isCollide:
                    self.projectiles.remove(projectile)
                    projectile.target_enemy.hit(self.damage[self.level] + self.general_upgrade["damage"][0]*0.2 + self.tower_upgrade["damage"][0]*0.4)

    def sell(self):
        return self.sell_price[self.level-1]
    

    def upgrade(self):
        if self.level < len(self.upgrade_price)-1:
            self.level += 1
            return self.upgrade_price[self.level-1]
        else:
            print("highest level")
            return 0

