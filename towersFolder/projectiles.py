import pygame
import math

class proj:
    def __init__(self, origin, target_enemy, projectile_imgs, velocity, projectile_type, width, height):
        self.proj_xCenter = origin.x + origin.width/2
        self.proj_yCenter = origin.y + origin.height/2
        self.target_enemy = target_enemy
        self.projectile_imgs = projectile_imgs
        self.velocity = velocity
        self.projectile_type = projectile_type
        self.distance_to_enemy = None
        self.delta_degree = None
        self.dx = None
        self.dy = None
        self.isCollide = False
        self.Paused = 1

    def draw(self, screen):

        if self.projectile_type == 1:
            self.draw_Arrow(screen)
        elif self.projectile_type == 2:
            print()

    def draw_Arrow(self, screen):
        
        self.distance_to_enemy = math.sqrt((self.proj_xCenter - (self.target_enemy.x + self.target_enemy.width/2))**2 + (self.proj_yCenter - (self.target_enemy.y + self.target_enemy.height/2))**2)
        
        self.dx = (self.proj_xCenter - (self.target_enemy.x + self.target_enemy.width/2))
        self.dy = (self.proj_yCenter - (self.target_enemy.y + self.target_enemy.height/2))

        
        if self.distance_to_enemy > 3:
            self.proj_xCenter -= (self.dx/self.distance_to_enemy) * self.velocity * self.Paused
            self.proj_yCenter -= (self.dy/self.distance_to_enemy) * self.velocity * self.Paused

            if self.dy < 0:
                if self.dx < 0:
                    self.delta_degree = (180 + math.degrees(math.asin(self.dx/self.distance_to_enemy)))*(-1)
                elif self.dx >= 0:
                    self.delta_degree = 180 - abs(math.degrees(math.asin(self.dx/self.distance_to_enemy)))

            elif self.dy >= 0:
                self.delta_degree = math.degrees(math.asin(self.dx/self.distance_to_enemy))#pygame rotate gos anticlockwise
            #print(self.dx,self.dy)
            #print(self.delta_degree)
            projectile_img = pygame.transform.rotate(self.projectile_imgs[0], self.delta_degree)

            screen.blit(projectile_img,
                        (self.proj_xCenter,
                         self.proj_yCenter))
        else:
            self.isCollide = True

    def get_distance(self):

        
        dx = self.x - self.target_enemy.x
        dy = self.y - self.target_enemy.y
