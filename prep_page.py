import pygame
import os
import in_game
from menuFolder.menu import menu
from levelsFolder.level_A import Map_A
from towersFolder.tower_A import Tower_A
from towersFolder.supportTower import supportTower_A

start_img = pygame.image.load(os.path.join("img/main_page_img","start_button.png"))
border_img = pygame.image.load(os.path.join("img/borders","b1.png"))
exit_img = pygame.image.load(os.path.join("img/prep_page","exit.png"))
tower_select_img = pygame.image.load(os.path.join("img/prep_page","tower_select.jpg"))

pygame.init()
pygame.font.init()

items_per_row = 5

class prepPage:
    def __init__(self, screen_width, screen_height, current_player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.bg = pygame.transform.scale(
            pygame.image.load(os.path.join(
                "img","main_page_bg.jpg")), (self.screen_width,self.screen_height))

        self.tower_slots = current_player.general_upgrades['tower_slots'][0]
        
        self.stw_width = 0.75 * self.screen_width
        self.stw_height = 0.8 * self.stw_width

        self.selected_tower = []

        self.allTowers = [Tower_A(), supportTower_A()]

        self.towerdisplay = {}

        for tower in self.allTowers:
            if current_player.towers_upgrades["{}".format(tower.id)]['unlocked'][0]:
                self.towerdisplay[tower.id] = [tower.tower_imgs[0], tower, 1]
            else:
                self.towerdisplay[tower.id] = [tower.locked_img, tower, 0]

        
        self.tower_islocked = []
        self.towers_img = [Tower_A().tower_imgs[0],supportTower_A().tower_imgs[0]]
        self.towers_obj = [Tower_A(), supportTower_A()]
        
        #stw resolution is always 1:0.8
        self.stw_items = [(0.004*self.stw_width,0.004*self.stw_height,0.19*self.stw_width,0.125*self.stw_height,
                           None,(252, 115, 3),
                           None,
                           1),
                          (0.004*self.stw_width,0.125*self.stw_height,0.19*self.stw_width,0.875*self.stw_height,
                           tower_select_img,None,
                           [(self.towerdisplay[1][0], self.towerdisplay[1][1], None, None, self.towerdisplay[1][2]),
                            (self.towerdisplay[2][0], self.towerdisplay[2][1], None, None, self.towerdisplay[2][2])]
                           ,2),
                          (0.19*self.stw_width,0.004*self.stw_height,0.81*self.stw_width,0.8125*self.stw_height,
                           None,(222, 51, 42),
                           None
                           ,3),
                          (0.19*self.stw_width,0.8125*self.stw_height,0.81*self.stw_width,0.1875*self.stw_height,
                           tower_select_img,None,
                           [(None,None,None,None),
                            (None,None,None,None),
                            (None,None,None,None),
                            (None,None,None,None),
                            (None,None,None,None),
                            (None,None,None,None)]
                           ,4),
                          (0.80*self.stw_width,0.8125*self.stw_height,0.20*self.stw_width,0.1875*self.stw_height,
                           tower_select_img,None,
                           [(start_img, "start", None, None)]
                           ,5),
                          (0.93*self.stw_width,0,0.07*self.stw_width,0.0875*self.stw_height,
                           exit_img,None,
                           [(None,"e",None,None)]
                           ,6)
                            ]

        self.stw = menu(0.125*self.screen_width, 0.108*self.screen_height,
                        self.stw_width, self.stw_height, self.stw_items, border_img, None,
                        None, None, None,
                        None, None, None,
                        None, (59, 64, 71), 2)



        
        self.gap = 0.02*self.screen_width
        self.button_width = ((self.screen_width - self.gap * (items_per_row+1)) / items_per_row)*0.8
        self.button_height = 0.8*self.button_width
        
        self.level_one_menu_items = [(Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None)]
        
        self.level_one_menu = menu(0.05*self.screen_width, 0.05*self.screen_height,         #need to increase the y by at least this height
                         0.9*self.screen_width,  2.6*(self.button_height + self.gap), self.level_one_menu_items, None, (41, 51, 61),
                         None, None, None,
                         self.button_width, self.button_height, self.gap,
                         None, None
                         )

        self.level_two_menu_items = [(Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None),
                                     (Map_A().bg, Map_A, None, None)]
        
        self.level_two_menu = menu(0.05*self.screen_width, 2*(0.05*self.screen_height) + 2.6*(self.button_height + self.gap),         #need to increase the y by at least this height
                         0.9*self.screen_width,  2.6*(self.button_height + self.gap), self.level_one_menu_items, None, (41, 51, 61),
                         None, None, None,
                         self.button_width, self.button_height, self.gap,
                         None, None
                         )

        self.exit_menu_item = [(exit_img, "e", None, (255,255,255))]
        self.exit_menu = menu(self.screen_width*0.95, 0,
                         self.screen_width*0.05, self.screen_width*0.05, self.exit_menu_item, None, None,
                         None, None, None,
                         self.screen_width*0.05, self.screen_width*0.05, 0,
                         None, None)

        
        self.drag_x = 0                         #difference from origin to draged position, compared with top left corners
        self.drag_y = 0
        self.drag = False

        self.map_selection_surface = pygame.Surface((self.screen_width, 900),pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.start = True

        self.selected_level = None
        self.selected_map = None
        self.selected_map_num = None
        self.isSelected_map = False
        self.gameStart = False



    def draw(self, cursor_pos):
        self.level_one_menu.level_menu_withSetItemPerRow(self.map_selection_surface, items_per_row, "Level 1")
        self.level_two_menu.level_menu_withSetItemPerRow(self.map_selection_surface, items_per_row, "Level 2")
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.map_selection_surface, (self.drag_x,self.drag_y))


        self.exit_menu.draw_horizontal_small(self.screen)
        
        if self.isSelected_map:
            self.get_set_tower(cursor_pos, self.stw)
        


    def run(self):
        while self.start:

            self.clock.tick(20)

            if self.gameStart:
                return (self.selected_map, self.selected_tower)
            
            
            cursor_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False
                  
                if event.type == pygame.MOUSEBUTTONDOWN:

                    cursor_pos = pygame.mouse.get_pos()
                    offset_x = self.drag_x - cursor_pos[0]
                    offset_y = self.drag_y - cursor_pos[1]
                    normal_coord = (abs(offset_x), abs(offset_y))

                    if event.button == 1:

                        if self.exit_menu.buttons[0].click(cursor_pos[0],cursor_pos[1]) == "e":
                            return "e"
                        
                        if not self.selected_map:
                            
                            if self.cursor_in_range(normal_coord, self.level_one_menu):
                                selected = self.get_set_map(normal_coord, self.level_one_menu)
                                if selected != None:
                                    self.selected_level = str(1)
                                    self.selected_map = selected[0]
                                    self.selected_map_num = selected[1]
                                    
                            if self.cursor_in_range(normal_coord, self.level_two_menu):
                                selected = self.get_set_map(normal_coord, self.level_two_menu)
                                if selected != None:
                                    self.selected_level = str(1)
                                    self.selected_map = selected[0]
                                    self.selected_map_num = selected[1]
                                      
                    if event.button == 3:
                        self.drag = True
                        cursor_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.drag = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.drag:
                        self.drag_y = cursor_pos[1] + offset_y

                        if self.drag_y > 0:
                            self.drag_y = 0
                        if self.drag_y < -self.screen_height:
                            self.drag_y = -self.screen_height

            
            self.draw(cursor_pos)
            pygame.display.update()
        pygame.quit()


    
            
    def cursor_in_range(self, cursor, obj):
        if obj.x < cursor[0] < obj.x + obj.menu_width:
            if obj.y < cursor[1] < obj.y + obj.menu_height:
                return True
        return False



    def get_set_map(self, cursor, menu):
        offset_x = menu.ori_x
        offset_y = menu.ori_y
        for x, button in enumerate(menu.buttons):
            selected_map = button.click(cursor[0]-offset_x,cursor[1]-offset_y)
            if selected_map != None:
                self.isSelected_map = True
                return (selected_map, str(x+1))

    def get_set_tower(self, cursor, menu):

        self.stw.displayers[0].displayer_items = self.selected_level+'-'+self.selected_map_num
        self.stw.displayers[2].displayer_items = self.selected_map().bg             #map display
        self.stw.drawDisplayers(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.start = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (menu.displayers[1].x + menu.ori_x < cursor[0] < menu.displayers[1].x + menu.ori_x + menu.displayers[1].menu_width) and (menu.displayers[1].y + menu.ori_y < cursor[0] < menu.displayers[1].y + menu.ori_y + menu.displayers[1].menu_height):
                        offset_x = menu.displayers[1].x + menu.ori_x
                        offset_y = menu.displayers[1].y + menu.ori_y
                        for t1button in menu.displayers[1].buttons:
                            v = t1button.click(cursor[0]-offset_x,cursor[1]-offset_y)
                            if v != None and v.id not in self.selected_tower:
                                if len(self.selected_tower) < self.tower_slots:
                                    self.selected_tower.append(v.id)
                                    for t4button in menu.displayers[3].buttons:
                                        if t4button.button_img == None:
                                            t4button.button_img = t1button.button_img
                                            t4button.button_obj = t1button.button_obj
                                            #print(t4button.x, t4button.button_width)
                                            #print(t4button.y, t4button.button_height)
                                            break
                                else:
                                    print('cant add more tower')
                                
                        
                        

                    else:
                        offset_x = menu.ori_x
                        offset_y = menu.ori_y
                        

                        for t4button in menu.displayers[3].buttons:
                            v1 = t4button.click(cursor[0]-offset_x,cursor[1]-offset_y)
                            if v1 != None:
                                v1 = v1.id
                                self.selected_tower.remove(v1)
                                t4button.button_img = t4button.button_obj = None
                                
                        
                        if menu.displayers[5].buttons[0].click(cursor[0]-offset_x,cursor[1]-offset_y) == "e":
                            self.selected_map = None
                            self.isSelected_map = False

                        elif menu.displayers[4].buttons[0].click(cursor[0]-offset_x,cursor[1]-offset_y) == "start":
                            if self.selected_tower:
                                self.gameStart = True
                            else:
                                print("need at least one tower")




