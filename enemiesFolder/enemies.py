import pygame
import math
from findpath import find_path
import random


class enemy:
    def __init__(self, current_path, current_map, tileWidth, tileHeight):
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        
        self.pathPos = 0

        self.timer = 0

        self.animation = 1                      #img num starts from 1
        self.da = 50                        #rate of animation, the smaller the faster
        self.img = None
        self.enemy_imgs = []
        self.direction = None
        self.path = current_path
        self.newPath = None

        self.current_map = current_map

        self.map_changed = False

        self.oldPath = None

        self.projectile_collide = False

        self.isDead = False

        self.not_pause = 1

    def draw(self, screen):                 #main function

        self.draw_healthBar(screen)
        self.move()
        
        current_img = self.img_count()

        screen.blit(current_img, (self.x, self.y))


        if self.isDead is True:
            self.onDeath()
    
    def draw_healthBar(self, screen):

        healthBar_surface = pygame.Surface((self.width+self.width/5, 3))
        healthBar_surface.fill((230,50,50))
        pygame.draw.rect(healthBar_surface, (17, 240, 20),
                         (0, 0,
                          (healthBar_surface.get_width()/self.max_health)*self.current_health
                          , healthBar_surface.get_height()),0)
        screen.blit(healthBar_surface, (self.x - ((healthBar_surface.get_width()/self.max_health)*self.current_health - self.width)/2, self.y - 4))
        
    def get_newPath(self):
        x = self.x
        y = self.y

        if self.direction == 2:
            x = self.x + self.width
        elif self.direction == 0:
            y = self.y + self.height
            
            
        
        p = find_path(self.current_map, (int(x/self.tileWidth)+1, int(y/self.tileHeight)+1)
                       , (self.path[-2][0]+1, self.path[-2][1]+1))
        p.append(self.path[-1])

        return p

    def img_count(self):                        #for animation

        self.timer += 1

        if self.timer > self.da:
            
            if self.animation >= len(self.enemy_imgs[self.direction])-1:
                self.animation = 0
                    
            else:
                self.animation += 1

            self.timer = 0

        return self.enemy_imgs[self.direction][self.animation]
        
    def collide(self, proj_x, proj_y):              #projectile
        if proj_x < self.x + self.width and proj_x > self.x:
            if proj_y < self.y +self.height and proj_y > self.y:
                return True
        return False



    def move(self):
        #print("i am self.pathPos", self.pathPos)
        #print("i am self.path", self.path[self.pathPos])
        #print(self.x, self.y)
        #print("i am len(self.path)", len(self.path)-1)
        if self.pathPos >= len(self.path)-1:      #when enemy goes to the destination
            #dx = self.path[-1]+40
            self.x = self.path[-1][0]*self.tileWidth
            self.y = self.path[-1][1]*self.tileHeight
            
            dx = dy = 0
        else:
            if self.map_changed == True:

                self.path = self.get_newPath()
                self.pathPos = 0

                self.map_changed = False

            dx = self.path[self.pathPos+1][0] - self.path[self.pathPos][0]
            dy = self.path[self.pathPos+1][1] - self.path[self.pathPos][1]

            self.x += dx*self.ds * self.not_pause             #enemy speed
            self.y += dy*self.ds * self.not_pause

            random_x = random.randint(int(((self.tileWidth-self.width)/2)-6), int(((self.tileWidth-self.width)/2)+6))
            random_y = random.randint(int(((self.tileHeight-self.height)/2)-6), int(((self.tileHeight-self.height)/2)+6))
            if dx > 0:
                self.direction = 2                      #right
                if self.x >= self.path[self.pathPos+1][0]*self.tileWidth + random_x:
                    self.pathPos += 1
            elif dx < 0:
                self.direction = 1                      #left
                if self.x <= self.path[self.pathPos+1][0]*self.tileWidth + random_x:
                    self.pathPos += 1
            elif dy > 0:
                self.direction = 0                      #down
                if self.y >= self.path[self.pathPos+1][1]*self.tileHeight + random_y:
                    self.pathPos += 1
            elif dy < 0:
                self.direction = 3                      #top
                if self.y <= self.path[self.pathPos+1][1]*self.tileHeight + random_y:
                    self.pathPos += 1

    def hit(self, damage):
        
        self.current_health -= damage
        
        if self.current_health <= 0:
            self.isDead = True

    def onDeath(self):
        return self.loot
