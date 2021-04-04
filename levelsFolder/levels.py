import pygame
import os
import time
import sys

from findpath import find_path
from enemiesFolder.enemy_A import *
from menuFolder.menu import *
from towersFolder.tower_A import Tower_A
from towersFolder.supportTower import supportTower_A
from .spawners import spawner



life_img = pygame.image.load(os.path.join("img/inGame_topBar","life.png"))
gold_img = pygame.image.load(os.path.join("img/inGame_topBar","gold.png"))
wave_img = pygame.image.load(os.path.join("img/inGame_topBar","wave.png"))

button_length = 17
############## need tower img for replacement ###############
upgrade_img = pygame.image.load(os.path.join("img/tower_menu","upgrade.png"))
sellTower_img = pygame.image.load(os.path.join("img/tower_menu","sell_tower.png"))

sup_menu_button_length = 30
pause_img = pygame.image.load(os.path.join("img/sup_menu", "pause.png"))
speedUp_img = pygame.image.load(os.path.join("img/sup_menu", "speedUp.png"))
nextWave_img = pygame.image.load(os.path.join("img/sup_menu", "nextWave.png"))

defeat_img = pygame.image.load(os.path.join("img/endgamemenu","defeat.png"))
victory_img = pygame.image.load(os.path.join("img/endgamemenu","victory.png"))

class MapTile:
    def __init__(self, name, x, y, obj):
        self.name = name
        self.x = x
        self.y = y
        self.obj = obj


####################    GRID    #####################

class road:
    def __init__(self, x, y, tileWidth, tileHeight, screen, _towers):
        self.selected = False
        self.xpos = x
        self.ypos = y
        self.x = self.xpos * tileWidth
        self.y = self.ypos * tileHeight
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.screen = screen
        self.menu_items = []
        self.imported_towers = None
        self.all_towers = [Tower_A(), supportTower_A()]
        for x in self.all_towers:
            if x.id in _towers:
                self.menu_items.append((x.tower_imgs[0], x, None, None))
        self.menu = menu(self.x + (tileWidth-(button_length+2)*len(self.menu_items))/2, self.y-12,
                         button_length*len(self.menu_items)+(len(self.menu_items)+1)*2, button_length, self.menu_items, None, None,
                         None, None, None,
                         button_length, button_length, 2,
                         None, None,
                         )
    def draw(self):
        if self.selected is True:
            surface = pygame.Surface((self.tileWidth, self.tileHeight))
            surface.fill((32, 209, 19))
            surface.set_alpha(120)
            self.screen.blit(surface,(self.x,self.y))
            self.menu.draw_horizontal_small(self.screen)
            

class block:
    def __init__(self, x, y, tileWidth, tileHeight, screen):
        self.selected = False
        self.xpos = x
        self.ypos = y
        self.x = self.xpos * tileWidth
        self.y = self.ypos * tileHeight
        self.screen = screen
        self.menu_items = []
        self.menu = menu(self.x, self.y,
                         0, 0, self.menu_items, None, None,
                         None, None, None,
                         button_length, button_length, 2,
                         None, None,
                         )

    def draw(self):
        if self.selected is True:
            self.menu.draw_horizontal_small(self.screen)
            print("deadend")
        self.selected = False



####################    LEVEL    #####################



class level:
    def __init__(self):
        
        self.enemies = []
        self.towers = []

        self._towers = None

        self.inGameMoney = 20
        self.life = 1000
        
        self.mapChanged = True
        self.path = None
        self.plop_tower = False
        
        self.wave_timer = time.time() - 23
        self.current_wave = 0
        self.wave_display = 0
        
        self.spawners = []

        self.drag_x = None
        self.drag_y = None

        self.timer = time.time()

        self.fps_multiplier = 1

        self.win = False
        self.lost = False
        self.withdrawn = False

        self.alpha = 0

        self.isPaused = False
        
        #speedup and pause
        self.sup_menu_items = [(nextWave_img, "nextWave", None, None), (speedUp_img, "speedUp", None, None), (pause_img, "pause", None, None)]
        self.sup_menu = menu(None, None,
                             sup_menu_button_length*len(self.sup_menu_items)+(len(self.sup_menu_items)+1)*2, sup_menu_button_length, self.sup_menu_items, None, None,
                             None, None, None,
                             sup_menu_button_length, sup_menu_button_length, 2,
                             None, None,
                             )

        self.exit_button = button(upgrade_img, 'e', None, None)

        self.game_surface = pygame.Surface((920,680),pygame.SRCALPHA)

    def spawn_enemy(self, current_level_Map):
        if self.current_wave < len(self.waves)+1:
            if time.time() - self.wave_timer >= 25/self.fps_multiplier:
                current_spawner = spawner(self.waves[self.current_wave], self.path, current_level_Map, self.tileWidth, self.tileHeight)
                self.spawners.append(current_spawner)
                self.wave_timer = time.time()
                self.current_wave += 1
                self.wave_display += 1
            
            if self.spawners:
                if not self.isPaused:
                    for _spawner in self.spawners:
                        if _spawner.spawn(self.enemies):
                            self.spawners.remove(_spawner)
                else:
                    print('paused')

    def get_path(self, current_level_Map):
        
        p = find_path(current_level_Map, self.startPos, self.endPos)
        return p

    def init_grids(self, screen, current_level_Map):
        for row in range(self.mapHeight):                       #grid become a tile object
            for column in range(self.mapWidth):
                if current_level_Map[row][column] == 1:
                    self.grids[row-1][column-1] = MapTile("road", column-1, row-1, road(column-1, row-1, self.tileWidth, self.tileHeight, screen, self._towers))       
                elif current_level_Map[row][column] == 0:
                    self.grids[row-1][column-1] = MapTile("block", column-1, row-1, block(column-1, row-1, self.tileWidth, self.tileHeight, screen))
                    
    def draw_grids(self, screen, current_level_Map):
        tileWidth, tileHeight, tileMargin = self.tileWidth, self.tileHeight, self.tileMargin
        line_sep = self.tileWidth + self.tileMargin                 #seperation of lines
        for row in range(self.mapHeight-1):            #Tiling land and sea
            for column in range(self.mapWidth-1):
                if current_level_Map[row][column] == 1:
                    color = (58,199,199) 
                elif current_level_Map[row][column] == 0:
                    color = (84,81,72)
                
                pygame.draw.rect(
                    screen, color, 
                    [(tileMargin + self.tileWidth) * (column-1) + tileMargin,
                    (tileMargin + tileHeight) * (row-1) + tileMargin,
                    tileWidth, tileHeight])
                
                #40 is line seperation
                
                pygame.draw.lines(screen, (255,255,255), True,
                                  [(row,column*self.tileWidth),
                                  (self.mapWidth*self.tileWidth,column*self.tileWidth)],1)
                pygame.draw.lines(screen, (255,255,255), True,
                                [(column*self.tileHeight,row),
                                (column*self.tileHeight,self.mapHeight*self.tileHeight)],1)
                     
                
        #self.drawState = 0
        
    def drawObjects(self, screen, current_path, current_level_Map):
        for enemy in self.enemies:
            enemy.draw(screen)                                          #draw enemy 
            if enemy.pathPos >= len(enemy.path)-1:                      #delete enemy
                self.enemies.remove(enemy)
                self.life -= 1
            if enemy.isDead is True:
                self.inGameMoney += enemy.onDeath()
                self.enemies.remove(enemy)  

        for tower in self.towers:                                #draw tower
            self.grids[tower.ypos][tower.xpos] = MapTile("tower", tower.xpos, tower.ypos, tower)
            tower.draw(screen)
            if tower.type == "attack":
                tower.attack(screen, self.enemies)
            elif tower.type == "support":
                tower.support(self.towers)

            if tower.isUpgrade is True:
                if self.inGameMoney >= tower.upgrade_price[tower.level]:
                    self.inGameMoney -= tower.upgrade()
                    tower.isUpgrade = False

        for row in range(self.mapHeight-1):
            for column in range(self.mapWidth-1):
                if self.grids[row][column].name != "tower":
                    self.grids[row][column].obj.draw()


    def plopTower(self, x, y, new_tower, current_player):
        self.temp_Map[y+1][x+1] = 0
        if self.get_path(self.temp_Map) != []:
            for enemy in self.enemies:
                if enemy.get_newPath() == []:
                    self.temp_Map[y+1][x+1] = 1
                    return False
                if enemy.x <= x*self.tileWidth+self.tileWidth and enemy.x >= (x)*self.tileWidth:
                    if enemy.y <= (y)*self.tileHeight+self.tileHeight and enemy.y >= (y)*self.tileHeight:
                        self.temp_Map[y+1][x+1] = 1
                        return False
            new_tower.xpos = x
            new_tower.ypos = y
            new_tower.x = x*self.tileWidth
            new_tower.y = y*self.tileHeight
            new_tower.general_upgrade = current_player.general_upgrades
            new_tower.tower_upgrade = current_player.towers_upgrades[f"{new_tower.id}"]
            self.towers.append(new_tower)
            self.inGameMoney -= new_tower.upgrade_price[0]
            self.mapChanged = True

        else:
            self.temp_Map[y+1][x+1] = 1



    def remove_tower(self, x, y, tower):
        self.inGameMoney += tower.sell()
        self.temp_Map[y+1][x+1] = 1
        self.towers.remove(tower)
        self.mapChanged = True

    def pause(self, button):
        self.isPaused = True
        button.button_img = upgrade_img
        button.button_obj = "resume"
        for enemy in self.enemies:
            enemy.not_pause = 0
        for tower in self.towers:
            tower.isPaused = True
        self.wave_timer = sys.maxsize

    def resume(self, button):
        self.isPaused = False
        button.button_img = pause_img
        button.button_obj = "pause"
        for enemy in self.enemies:
            enemy.not_pause = 1
        for tower in self.towers:
            tower.isPaused = False
        self.spawn_timer = self.stime

    def nextWave(self):
        if self.current_wave != 0:
            self.wave_timer = time.time()-25
        else:
            print('not started')

        
    def checkiflost(self):
        if self.life <= 0:
            self.lost = True
        
        



########################## Draw Top Bar #########################

    def drawMenu(self, screen, screen_width, screen_height):
        button_length = screen_height/22
        txt_length = button_length*3
        topBar_menu_item = [(wave_img, self.wave_display, None, (191, 145, 17)), (gold_img, self.inGameMoney, None, (191, 145, 17)), (life_img, self.life, None, (191, 145, 17))]
        topBar_menu = menu(0.4*screen_width, 0,
                           screen_width/1.7, screen_height/11, topBar_menu_item, None, None,
                           int(button_length) + txt_length, int(button_length), 0.6,
                           int(button_length), int(button_length), (screen_width/2 - (len(topBar_menu_item) * (int(button_length) + txt_length))) / (len(topBar_menu_item) + 1),
                           txt_length, (255, 255, 255),
                           )
        topBar_menu.drawMenuWithTxt(screen)


        #Speed Up Pause
        self.sup_menu.ori_x = screen_width*0.8 - ((len(self.sup_menu_items)*(sup_menu_button_length+2))-40)/2
        self.sup_menu.ori_y = screen_height*0.857
        self.sup_menu.draw_horizontal_small(screen)

        #exit button
        self.exit_button.x = (11/12) * screen_width
        self.exit_button.y = screen_height / 44
        self.exit_button.button_width = screen_height/22
        self.exit_button.button_height = screen_height/22
        self.exit_button.drawGridButtons(screen)

        

############################### draw game ############################

    def draw_level(self, screen, screen_width, screen_height, current_level_Map):
        
        if not self.win and not self.lost and not self.withdrawn:
            
            self.game_surface.blit(self.bg,(0,0))

            #self.draw_grids(self.game_surface, current_level_Map)
            
            if self.path == None:
                self.init_grids(self.game_surface, current_level_Map)
                self.path = self.get_path(current_level_Map)

            if self.mapChanged is True:
                self.init_grids(self.game_surface, current_level_Map)
                self.path = self.get_path(current_level_Map)
                for enemy in self.enemies:
                    enemy.current_map = current_level_Map
                    enemy.map_changed = True
                
                self.mapChanged = False
            
            self.spawn_enemy(current_level_Map)

            self.drawMenu(screen, screen_width, screen_height)
            self.drawObjects(self.game_surface, self.path, current_level_Map)

            self.checkiflost()

        else:
            if self.win:
                v = self.fadeOut(screen, screen_width, screen_height, 1)
            elif self.lost:
                v = self.fadeOut(screen, screen_width, screen_height, 0)
            elif self.withdrawn:
                v = self.fadeOut(screen, screen_width, screen_height, 2)
            if v != None:
                return v
        
        
    def onWin(self, screen, screen_width, screen_height):
        menu_items = [(gold_img, int(self.inGameMoney), None, (170, 111, 17))]
        txt_length = 30
        button_gap = 10
        win_menu = menu((0.15)*screen_width, (0.2)*screen_height,
                         0.7*screen_width, 0.6*screen_height, menu_items, victory_img, None,
                         0.6*0.7*screen_width, (0.6*screen_height - 6*button_gap) / 6, 0.8,
                         (0.6*screen_height - 6*button_gap) / 6, (0.6*screen_height - 6*button_gap) / 6, button_gap,
                         txt_length,(0,0,0))    
        win_menu.drawEndGameMenu(screen)
        
        if time.time() - self.timer >= 4:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return (self.inGameMoney)

        

    def onLose(self, screen, screen_width, screen_height):
        menu_items = [(gold_img, int(self.inGameMoney*0.7), None, (170, 111, 17))]
        txt_length = 30
        button_gap = 10
        lost_menu = menu((0.15)*screen_width, (0.2)*screen_height,
                         0.7*screen_width, 0.6*screen_height, menu_items, defeat_img, None,
                         0.6*0.7*screen_width, (0.6*screen_height - 6*button_gap) / 6, 0.8,
                         (0.6*screen_height - 6*button_gap) / 6, (0.6*screen_height - 6*button_gap) / 6, button_gap,
                         txt_length,(0,0,0))    
        lost_menu.drawEndGameMenu(screen)
        if time.time() - self.timer >= 4:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return (self.inGameMoney*0.7)

    def onWithDraw(self, screen, screen_width, screen_height):
        menu_items = [(gold_img, int(self.inGameMoney*0.2), None, (170, 111, 17))]
        txt_length = 30
        button_gap = 10
        lost_menu = menu((0.15)*screen_width, (0.2)*screen_height,
                         0.7*screen_width, 0.6*screen_height, menu_items, defeat_img, None,
                         0.6*0.7*screen_width, (0.6*screen_height - 6*button_gap) / 6, 0.8,
                         (0.6*screen_height - 6*button_gap) / 6, (0.6*screen_height - 6*button_gap) / 6, button_gap,
                         txt_length,(0,0,0))    
        lost_menu.drawEndGameMenu(screen)
        if time.time() - self.timer >= 4:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return (self.inGameMoney*0.2)

    def fadeOut(self, screen, screen_width, screen_height, endState):
        fade_surface = pygame.Surface((screen_width, screen_height))

        if self.alpha < 170:
            self.alpha += 6
            fade_surface.set_alpha(self.alpha)
            
        screen.blit(fade_surface, (0,0))

        if self.alpha >= 170:
            if endState == 1:
                value = self.onWin(screen, screen_width, screen_height)
            elif endState == 0:
                value = self.onLose(screen, screen_width, screen_height)
            elif endState == 2:
                value = self.onWithDraw(screen, screen_width, screen_height)
            if value != None:
                return value
            
            









        
