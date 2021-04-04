import pygame
import time
import os
from levelsFolder.level_A import Map_A

pygame.init()
pygame.font.init()
#Map_A size is 40*23 width 40*17 height
#Map_A size is 920 x 680
class game:
    def __init__(self, screen_width, screen_height, current_player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.fps_multiplier = 0
        self.start = True
        self.currentSelected = None
        self.current_player = current_player

        self.drag_x = 0                         #difference from origin to draged position, compared with top left corners
        self.drag_y = 0
        self.drag = False
        
        self.current_level = Map_A()
        self.towers_id = None
        self.enter = False


    def run(self):
        
        while self.start:
            self.clock.tick(self.fps)
            cursor_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.start = False
                  
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.current_level.win and not self.current_level.lost and not self.current_level.withdrawn:
                        cursor_pos = pygame.mouse.get_pos()
                        offset_x = self.drag_x - cursor_pos[0]
                        offset_y = self.drag_y - cursor_pos[1]
                        normal_coord = (abs(offset_x), abs(offset_y))
                        if event.button == 1:
                            if self.current_level.exit_button.click(cursor_pos[0], cursor_pos[1]) == 'e':
                                self.current_level.withdrawn = True
                            new_grid = self.current_level.grids[int(normal_coord[1]/self.current_level.tileWidth)][int(normal_coord[0]/self.current_level.tileHeight)]
                            if self.cursor_in_range(cursor_pos, self.current_level.sup_menu):
                                for button in self.current_level.sup_menu.buttons:
                                    if button.click(cursor_pos[0], cursor_pos[1]) == "pause":
                                        self.current_level.pause(button)
                                    elif button.click(cursor_pos[0], cursor_pos[1]) == "resume":
                                        self.current_level.resume(button)
                                    elif button.click(cursor_pos[0], cursor_pos[1]) == "speedUp":
                                        if self.fps < 60:
                                            self.fps *= 2
                                            self.current_level.fps_multiplier += 1
                                            for _spawner in self.current_level.spawners:
                                                _spawner.fps_multiplier += 1
                                            
                                        else:
                                            self.fps = 30
                                            self.current_level.fps_multiplier = 1
                                            for _spawner in self.current_level.spawners:
                                                _spawner.fps_multiplier = 1
                                    elif button.click(cursor_pos[0], cursor_pos[1]) == "nextWave":
                                        self.current_level.nextWave()
                            
                            elif self.currentSelected == None:
                                self.currentSelected = new_grid
                                self.currentSelected.obj.selected = True
                            elif (new_grid.x != self.currentSelected.x or new_grid.y != self.currentSelected.y or new_grid.name != self.currentSelected.name):
                                if self.currentSelected.name == "block":
                                    self.currentSelected.obj.selected = False
                                    self.currentSelected = new_grid
                                    self.currentSelected.obj.selected = True
                                elif not self.cursor_in_range(normal_coord, self.currentSelected.obj.menu):
                                    self.currentSelected.obj.selected = False
                                    self.currentSelected = new_grid
                                    self.currentSelected.obj.selected = True
                            if not self.cursor_in_range(cursor_pos, self.current_level.sup_menu):
                                if self.currentSelected.obj.menu.x != None:
                                    if self.cursor_in_range(normal_coord, self.currentSelected.obj.menu):
                                        for button in self.currentSelected.obj.menu.buttons:
                                            if self.currentSelected.name == "tower" and button.x != None:
                                                if button.click(normal_coord[0], normal_coord[1]) == "upgrade":
                                                    
                                                    self.currentSelected.obj.isUpgrade = True
                                                elif button.click(normal_coord[0], normal_coord[1]) == "sell":
                                                
                                                    self.current_level.remove_tower(self.currentSelected.x, self.currentSelected.y, self.currentSelected.obj)
                                                    self.currentSelected = None
                                            elif self.currentSelected.name == "road" and button.x != None:
                                                
                                                new_tower = button.click(normal_coord[0], normal_coord[1])
                                                if new_tower != None:
                                                    self.current_level.plopTower(self.currentSelected.x, self.currentSelected.y, new_tower, self.current_player)
                                              
                        elif event.button == 3:
                            self.drag = True
                            if self.currentSelected != None:
                                self.currentSelected.obj.selected = False
                                self.currentSelected = None
                            
                            cursor_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if not self.current_level.win and not self.current_level.lost:
                        if event.button == 3:
                            self.drag = False
                            self.current_level.onDrag = False

                elif event.type == pygame.MOUSEMOTION:
                    if not self.current_level.win and not self.current_level.lost:
                        if self.drag:
                            self.drag_x = cursor_pos[0] + offset_x
                            self.drag_y = cursor_pos[1] + offset_y
                            
                            
                            if self.drag_x > 0:
                                self.drag_x = 0
                            if self.drag_y > 0:
                                self.drag_y = 0
                            if self.drag_x < self.screen_width - (self.current_level.mapWidth-2)*self.current_level.tileWidth:
                                self.drag_x = self.screen_width - (self.current_level.mapWidth-2)*self.current_level.tileWidth
                            if self.drag_y < self.screen_height - (self.current_level.mapHeight-2)*self.current_level.tileHeight:
                                self.drag_y = self.screen_height - (self.current_level.mapHeight-2)*self.current_level.tileHeight

            self.screen.blit(self.current_level.game_surface, (self.drag_x,self.drag_y)) 
            v = self.drawGame()

            if v != None:
                return v

            pygame.display.flip()
        
        pygame.quit()

    def drawGame(self):
        self.current_level._towers = self.towers_id
        
        v = self.current_level.draw_level(self.screen, self.screen_width, self.screen_height, self.current_level.temp_Map)

        if v != None:
            return v


    def cursor_in_range(self, cursor, obj):
        if obj.x < cursor[0] < obj.x + obj.menu_width:
            if obj.y < cursor[1] < obj.y + obj.menu_height:
                return True
        return False
