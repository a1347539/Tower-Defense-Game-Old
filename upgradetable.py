#Initialize
import pygame
import json

pygame.init()

all_towers = ['general_upgrades',"1","2"]

#Style Variable
tower_padding_top = 30
tower_size = 40
lineToMainline_width = 2

upgrade_padding_top = 20
upgrade_padding_LR = 15
upgrade_size = 30
lineToTower_width = 1

start_padding_left = 30
mainLine_xStart = 0
mainLine_width = 3
mainLine_yPos = 150 * len(all_towers)/2

#Generating Button and Lines array
tree_length = start_padding_left

#Upgrade count
upgrade_xNum = 3
upgrade_yNum = 2



#Classes
class buttons:
    def __init__(self, x, y, width, height, Object, player, color=(255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Object = Object
        self.color = color
        self.player = player

        

    def click(self, cursor):
        if (self.x < cursor[0] <= self.x + self.width) :
            if (self.y < cursor[1] <= self.y + self.height) :
                if self.Object != "e":
                    if self.Object == 'general_upgrades' or self.Object[0] ==  'general_upgrades':
                        branchDict = self.player.general_upgrades
                        dictKeys = list(self.player.general_upgrades.keys())
                        
                        if isinstance(self.Object, list):
                            previous_node_info = branchDict[dictKeys[self.Object[1]+1+3*(self.Object[2]-1)]]
                            node_info = branchDict[dictKeys[self.Object[1]+1+3*(self.Object[2])]]

                        if isinstance(self.Object, str):
                            if len(branchDict['tower_slots'][1]) > branchDict['tower_slots'][0]:
                                if self.player.money > branchDict['tower_slots'][1][branchDict['tower_slots'][0]]:
                                    self.player.money -= branchDict['tower_slots'][1][branchDict['tower_slots'][0]]
                                    branchDict['tower_slots'][0] += 1
                                    print(branchDict['tower_slots'][0])
                                else:
                                    print("not enough money")
                            else:
                                print("highes level")

                        elif self.Object[2] == 0 and node_info[0]//2 >= branchDict['tower_slots'][0]:
                            print("upgrade the previous node")
                        
                        elif self.Object[2] != 0 and previous_node_info[0] < 4:
                            print("upgrade the previous node to level 4")

                        else:
                            if len(node_info[1]) == node_info[0]:
                                print("highest level")
                            elif len(node_info[1]) > node_info[0]:
                                if self.player.money > node_info[1][node_info[0]]:
                                    self.player.money -= node_info[1][node_info[0]]
                                    node_info[0] += 1
                                    print(node_info[0])
                                else:
                                    print("not enough money")

                    else:
                        branchDict = self.player.towers_upgrades[self.Object[0]]
                        dictKeys = list(self.player.towers_upgrades[self.Object[0]].keys())
                        
                        if len(self.Object) > 2:
                            previous_node_info = branchDict[dictKeys[self.Object[1]+1+3*(self.Object[2]-1)]]
                            node_info = branchDict[dictKeys[self.Object[1]+1+3*(self.Object[2])]]

                        if not branchDict['unlocked'][0] and len(self.Object) > 2:
                            print("unlock the tower")
                            
                        elif len(self.Object) == 1:
                            if not branchDict['unlocked'][0]:
                                if self.player.money > branchDict['unlocked'][1]:
                                    self.player.money -= branchDict['unlocked'][1]
                                    branchDict['unlocked'][0] = True
                                    print("tower unlocked")
                                else:
                                    print("not enough money")
                            else:
                                print("tower unlocked")
                            
                            
                        elif self.Object[2] != 0 and previous_node_info[0] < 4:
                            print("upgrade the previous node to level 4")
                            
                        else:
                            if len(node_info[1]) == node_info[0]:
                                print("highest level")
                            elif len(node_info[1]) > node_info[0]:
                                if self.player.money > node_info[1][node_info[0]]:
                                    self.player.money -= node_info[1][node_info[0]]
                                    node_info[0] += 1
                                    print(node_info[0])
                                else:
                                    print("not enough money")
                    
                return self.Object

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        


class lines: 
    def __init__(self, start_pos, end_pos, width=1, color=(127,127,127)): 
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        
    def draw(self, screen): 
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)


#pygame Setting
class upgrade_table:
    def __init__(self, screen, screen_width, screen_height, current_player):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.upgradeScreen_width = 150 * len(all_towers)
        self.upgradeScreen_height = 601
        self.upgradeScreen = pygame.Surface((self.upgradeScreen_width, self.upgradeScreen_height))

        self.clock = pygame.time.Clock()
        
        self.current_player = current_player
        
        self.drag_x = 0                         #difference from origin to draged position, compared with top left corners
        self.drag_y = 0
        self.drag = False


        
        self.Lines = []      #[(xStart, yStart),(xEnd, yEnd),w,color]
        self.Buttons = []    #[x,y,w,h,obj,color]

        self.start = True



    
    
    def run(self):
        self.init_shapes(tree_length)
        
        while self.start:
            self.clock.tick(10)
            cursor_pos = pygame.mouse.get_pos()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_pos = pygame.mouse.get_pos()
                    offset_x = self.drag_x - cursor_pos[0]
                    offset_y = self.drag_y - cursor_pos[1]
                    normal_coord = (abs(offset_x), abs(offset_y))
                    
                    if event.button == 1: 
                        for x in self.Buttons:
                            v = x.click(normal_coord)
                            if v == "e":
                                self.save_file()
                                return
                            
                    elif event.button == 3:
                        self.drag = True
                        cursor_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.drag = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.drag:
                        if self.screen_width < self.upgradeScreen_width:
                            self.drag_x = cursor_pos[0] + offset_x
                            if self.drag_x > 0:
                                self.drag_x = 0
                            if self.drag_x < self.screen_width - self.upgradeScreen_width:
                                self.drag_x = self.screen_width - self.upgradeScreen_width
                        if self.screen_height < self.upgradeScreen_height:
                            self.drag_y = cursor_pos[1] + offset_y
                    
                        if self.drag_y > 0:
                            self.drag_y = 0

                        if self.drag_y < self.screen_height - self.upgradeScreen_height:
                            self.drag_y = self.screen_height - self.upgradeScreen_height

            self.draw()

            pygame.display.flip()

        pygame.quit()

    def save_file(self):
        with open('playerFolder/playerdata/user.txt', 'r') as infile:
            infile = json.load(infile)
            infile["general_upgrades"] = self.current_player.general_upgrades
            infile["towers_upgrade"] = self.current_player.towers_upgrades
            
        with open('playerFolder/playerdata/user.txt', 'w') as outfile:
            json.dump(infile, outfile, indent=4)
            
    

    def draw(self):
        self.upgradeScreen.fill((53, 63, 74))
        for y in self.Lines: 
            y.draw(self.upgradeScreen)
        for x in self.Buttons: 
            x.draw(self.upgradeScreen)

        
        self.screen.blit(self.upgradeScreen, (self.drag_x+10,self.drag_y+10))

    def init_shapes(self, tree_length):
        for names in all_towers: 
            tower_xOrder = all_towers.index(names)
            direction = tower_xOrder % 2
            tree_width = upgrade_size*upgrade_xNum + upgrade_padding_LR*(upgrade_xNum-1)
            
            lineToMainline_xPos = tree_length + tree_width/2
            towerBox_xPos = tree_length+(tree_width-tower_size)/2
            lineToTower_xStart = lineToMainline_xPos
            lineToMainline_yStart = mainLine_yPos
            
            if direction == 0: 
                lineToMainline_yEnd = mainLine_yPos + tower_padding_top
                self.Lines.append(lines((lineToMainline_xPos,lineToMainline_yStart),(lineToMainline_xPos,lineToMainline_yEnd),lineToMainline_width))
                
                towerBox_yPos = lineToMainline_yEnd
                self.Buttons.append(buttons(towerBox_xPos,towerBox_yPos,tower_size,tower_size,names, self.current_player))
                
                lineToTower_yStart = lineToMainline_yEnd + tower_size
                lineToTower_yEnd = lineToTower_yStart + upgrade_padding_top
                
                for x in range(upgrade_xNum): 
                    upgrade_xPos = tree_length + upgrade_size*x + upgrade_padding_LR*x
                    lineToTower_xEnd = upgrade_xPos + upgrade_size / 2
                    self.Lines.append(lines((lineToTower_xStart,lineToTower_yStart),(lineToTower_xEnd,lineToTower_yEnd),lineToTower_width))
                    
                    for y in range(upgrade_yNum):
                        upgrade_yPos = lineToTower_yEnd + upgrade_size*y + upgrade_padding_top*y
                        self.Buttons.append(buttons(upgrade_xPos,upgrade_yPos,upgrade_size,upgrade_size,[names, x, y], self.current_player))
                        
                    for y in range(upgrade_yNum-1): 
                        lineToUpdate_yStart = lineToTower_yEnd + upgrade_size*(y+1) + upgrade_padding_top*y
                        lineToUpdate_yEnd = lineToUpdate_yStart + upgrade_padding_top
                        self.Lines.append(lines((lineToTower_xEnd,lineToUpdate_yStart),(lineToTower_xEnd,lineToUpdate_yEnd),lineToTower_width))
            
            if direction == 1: 
                lineToMainline_yEnd = mainLine_yPos - tower_padding_top
                self.Lines.append(lines((lineToMainline_xPos,lineToMainline_yStart),(lineToMainline_xPos,lineToMainline_yEnd),lineToMainline_width))
                
                towerBox_yPos = lineToMainline_yEnd - tower_size
                self.Buttons.append(buttons(towerBox_xPos,towerBox_yPos,tower_size,tower_size,names, self.current_player))
                
                lineToTower_yStart = towerBox_yPos
                lineToTower_yEnd = lineToTower_yStart - upgrade_padding_top
                
                for x in range(upgrade_xNum): 
                    upgrade_xPos = tree_length + upgrade_size*x + upgrade_padding_LR*x
                    lineToTower_xEnd = upgrade_xPos + upgrade_size / 2
                    self.Lines.append(lines((lineToTower_xStart,lineToTower_yStart),(lineToTower_xEnd,lineToTower_yEnd),lineToTower_width))
                    
                    for y in range(upgrade_yNum):
                        upgrade_yPos = lineToTower_yEnd - upgrade_size*(y+1) - upgrade_padding_top*y
                        self.Buttons.append(buttons(upgrade_xPos,upgrade_yPos,upgrade_size,upgrade_size,[names, x, y], self.current_player))
                        
                    for y in range(upgrade_yNum-1): 
                        lineToUpdate_yStart = lineToTower_yEnd - upgrade_size*(y+1) - upgrade_padding_top*y
                        lineToUpdate_yEnd = lineToUpdate_yStart - upgrade_padding_top
                        self.Lines.append(lines((lineToTower_xEnd,lineToUpdate_yStart),(lineToTower_xEnd,lineToUpdate_yEnd),lineToTower_width))
            
            mainLine_xEnd = tree_length+tree_width/2+1
            tree_length += tree_width

        self.Lines.append(lines((mainLine_xStart,mainLine_yPos),(mainLine_xEnd,mainLine_yPos),mainLine_width))
        self.Buttons.append(buttons(self.upgradeScreen_width*0.95, 0, 20, 20, "e", None, (255,255,255)))

        
