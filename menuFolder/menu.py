import pygame
import math
'''
obj can be obj, txt, string, img
'''
pygame.font.init()

class displayer:
    def __init__(self, x, y, width, height, img, color, displayer_items, Type):
        self.x = x
        self.y = y
        self.menu_width = width
        self.menu_height = height
        self.img = img
        self.color = color
        self.displayer_items = displayer_items
        self.Type = Type
        self.surface = pygame.Surface((self.menu_width,self.menu_height))
        self.buttons = []
        self.overdrawn = False
        

        if self.Type == 4 or self.Type == 5 or self.Type == 6:
            for displayer_item in self.displayer_items:
                self.buttons.append(button(displayer_item[0], displayer_item[1],
                                           displayer_item[2], displayer_item[3]
                                           ))
        elif self.Type == 2:
            for displayer_item in self.displayer_items:
                self.buttons.append(button(displayer_item[0], displayer_item[1],
                                           displayer_item[2], displayer_item[3],
                                           displayer_item[4]
                                           ))

    def drawDisplayers(self, screen, menu_x, menu_y):

        if self.img != None:
            img = pygame.transform.scale(self.img,(int(self.menu_width),int(self.menu_height)))
            self.surface.blit(img, (0,0))
        elif self.color != None:
            self.surface.fill(self.color)

        if self.Type == 1:
            font = pygame.font.SysFont('calibri', int(self.menu_height*0.7))
            text_surface = font.render(str(self.displayer_items), True, (255,255,255))
            self.surface.blit(text_surface, ((self.menu_width-text_surface.get_width()*1.4)/2, (self.menu_height-text_surface.get_height()*0.8)/2))
            
            self.overdrawn = False
        
        if self.Type == 2:
            towers_per_row = 2
            for x, button in enumerate(self.buttons):
                i = x%towers_per_row
                button.button_width = 0.3*self.menu_width
                button.button_height = 0.3*self.menu_width
                button.x = ((self.menu_width - len(self.buttons)*button.button_width)*(i+1)/(len(self.buttons)+1)) + (button.button_width*i)
                if i == 1:
                    x = (x-1)/2
                elif i == 0:
                    x = x/2
                button.y = (0.5*self.y) + (0.5*self.menu_width) * x

                button.drawGridButtons(self.surface)
                
            self.overdrawn = False

        elif self.Type == 3:

            img = pygame.transform.scale(self.displayer_items, (int(self.menu_width), int(self.menu_height)))
            self.surface.blit(img, (0,0))
            
            self.overdrawn = False

        elif self.Type == 4:
            screen.blit(self.surface, (self.x, self.y))
            for x, button in enumerate(self.buttons):
                button.button_width = button.button_height = 0.08*self.menu_width
                button.x =  self.x*0.85 + (((self.menu_width-len(self.buttons)*0.08*self.menu_width)/(len(self.buttons)+1))*(x+1) + x*0.08*self.menu_width)
                button.y = self.y + (self.menu_height - button.button_height)/2
                
                button.drawGridButtons(screen)
                
            self.overdrawn = True

        elif self.Type == 5:
            for button in self.buttons:
                button.button_width = 0.8*self.menu_width
                button.button_height = 0.6*self.menu_height
                button.x = self.x + (self.menu_width - button.button_width) / 2
                button.y = self.y + (self.menu_height - button.button_height) / 2
                button.drawGridButtons(screen)
                
            self.overdrawn = True

            
        elif self.Type == 6:
            for button in self.buttons:
                button.x = self.x
                button.y = self.y
                button.button_width = self.menu_width
                button.button_height = self.menu_height

            self.overdrawn = False

        if not self.overdrawn:
            screen.blit(self.surface, (self.x, self.y))
        


class button:
    def __init__(self, button_img, button_obj, button_surface_img, button_surface_color, unlocked = 1):
        self.x = None
        self.y = None
        self.button_width = None
        self.button_height = None
        self.surface_x = None
        self.surface_y = None
        self.surface_width = None
        self.surface_height = None
        self.button_txt_gap = None
        
        self.txt_color = None

        self.button_img = button_img
        self.button_obj = button_obj
        self.button_surface_img = button_surface_img
        self.button_surface_color = button_surface_color
        self.unlocked = unlocked
        
        if self.button_img != None:
            self.img_width = self.button_img.get_width()
            self.img_height = self.button_img.get_height()

    '''
    grid menu, sup menu, first page start menu 
    '''
    def drawGridButtons(self, screen):
        if self.button_img != None:
            img = pygame.transform.scale(self.button_img, (int(self.button_width), int(self.button_height)))
            screen.blit(img, (self.x, self.y))

    def drawWithObj(self, screen):                
        pass

    def drawWithTxt(self, screen):
        surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)

        if self.button_surface_img != None:
            bg = pygame.transform.scale(self.button_surface_img,(int(self.surface_width),int(self.surface_height)))
            surface.blit(bg, (0,0))
        elif self.button_surface_color != None:
            surface.fill(self.button_surface_color)
            
        img = pygame.transform.scale(self.button_img, (int(self.button_width), int(self.button_height)))
        surface.blit(img, (0, 0))
        font = pygame.font.SysFont('calibri', int(self.button_height*1))
        text_surface = font.render(str(self.button_obj), True, (self.txt_color))
        surface.blit(text_surface, ((self.surface_width*self.button_txt_gap, 0)))
        screen.blit(surface, (self.surface_x, self.surface_y))

    def drawInSurface(self, screen):
        img = pygame.transform.scale(self.button_img, (int(self.button_width), int(self.button_height)))
        screen.blit(img, (self.x, self.y))


    def drawWithString(self, screen):
        pass

    def click(self, cursor_x, cursor_y):
        if self.x <= cursor_x <= self.x + self.button_width:
            if self.y <= cursor_y <= self.y + self.button_height:
                if self.unlocked == 0:
                    print('locked')
                    return None
                else:
                    return self.button_obj

'''
menu_items stores all the parameters of class button
'''
class menu:
    def __init__(self, x, y,
                 menu_width, menu_height, menu_items, menu_img, menu_color,
                 button_surface_width, button_surface_height, button_txt_gap,
                 button_width, button_height, button_gap,
                 txt_length, txt_color,
                 Type = 1):
        
        self.ori_x = x
        self.ori_y = y
        self.menu_width = menu_width
        self.menu_height = menu_height
        self.menu_items = menu_items
        self.menu_img = menu_img
        self.menu_color = menu_color

        self.button_surface_width = button_surface_width
        self.button_surface_height = button_surface_height
        self.button_txt_gap = button_txt_gap

        self.button_width = button_width
        self.button_height = button_height
        self.button_gap = button_gap

        self.txt_length = txt_length
        self.txt_color = txt_color

        self.Type = Type

        self.buttons = []

        self.displayers = []

        self.x = None
        self.y = None


        self.evenMenu_button_gap = None
        if self.Type == 1:
            for menu_item in self.menu_items:
                self.buttons.append(button(menu_item[0],menu_item[1],menu_item[2],menu_item[3]))

        elif self.Type == 2:
            for menu_item in self.menu_items:
                self.displayers.append(displayer(menu_item[0],menu_item[1],
                                                 menu_item[2],menu_item[3],
                                                 menu_item[4],menu_item[5],
                                                 menu_item[6],menu_item[7]))
    '''
    grid menu, sup menu
    '''
    def draw_horizontal_small(self, screen):

        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        self.x = self.ori_x
        self.y = self.ori_y
        
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)
        screen.blit(surface, (self.ori_x, self.ori_y))
            
        for x, button in enumerate(self.buttons):
            button.surface_width = self.button_surface_width
            button.surface_height = self.button_surface_height
            button.x = self.x + (self.button_width + self.button_gap) * x
            button.y = self.y
            button.button_width = self.button_width
            button.button_height = self.button_height
            button.drawGridButtons(screen)

            

        
    '''
    first page start menu 
    '''
    def draw_vertical(self, screen):

        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        self.x = self.ori_y
        self.y = self.ori_y


        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)
        screen.blit(surface, (self.ori_y, self.ori_y))

        for x, button in enumerate(self.buttons):
            button.surface_width = self.button_surface_width
            button.surface_height = self.button_surface_height
            button.x = self.x
            button.y = self.y + (self.button_height + self.button_gap) * x
            button.button_width = self.button_width
            button.button_height = self.button_height
            
            button.drawGridButtons(screen)


    '''
    top bar
    '''
    def drawMenuWithTxt(self, screen):

        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        self.x = self.ori_x + self.button_gap
        self.y = self.ori_y
        self.surface_x = self.x
        self.surface_y = self.y
        
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)
        screen.blit(surface, (self.ori_x, self.ori_y))

        for x, button in enumerate(self.buttons):
            button.surface_x = self.surface_x + (self.button_width + self.txt_length + self.button_gap) * x
            button.surface_y = self.surface_y
            button.surface_width = self.button_surface_width
            button.surface_height = self.button_surface_height
            button.button_txt_gap = self.button_txt_gap
            #button.x = self.x + (self.button_width + self.txt_length + self.button_gap) * x
            #button.y = self.y
            button.button_width = self.button_width
            button.button_height = self.button_height
            button.txt_color = self.txt_color
            
            button.drawWithTxt(screen)

    '''
    lost menu
    '''
    def drawEndGameMenu(self, screen):
        
        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        self.x = self.ori_x
        self.y = self.ori_y + self.button_gap
        self.surface_x = self.x
        self.surface_y = self.y + 100
        
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)
        screen.blit(surface, (self.ori_x, self.ori_y))

        for x, button in enumerate(self.buttons):
            button.surface_x = self.surface_x + (self.menu_width - self.button_surface_width)/2
            button.surface_y = self.surface_y + (self.button_surface_height + self.button_gap) * x
            button.surface_width = self.button_surface_width
            button.surface_height = self.button_surface_height
            button.button_txt_gap = self.button_txt_gap
            #button.x = self.x + (self.menu_width - self.button_width)/2
            #button.y = self.y + (self.button_height + self.button_gap) * x
            button.button_width = self.button_width
            button.button_height = self.button_height
            button.txt_color = self.txt_color
            
            button.drawWithTxt(screen)


    def level_menu_withSetItemPerRow(self, screen, items_per_row, header):
                
        surface = pygame.Surface((self.menu_width,self.menu_height),pygame.SRCALPHA)
        self.x = self.ori_x
        self.y = self.ori_y + self.button_gap

        font = pygame.font.SysFont('calibri', int(self.button_height*0.70))
        text_surface = font.render(str(header), True, ((255,255,255)))
    
        
        
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)
        
        surface.blit(text_surface, ((self.menu_width*0.07,0)))
        
        for x, button in enumerate(self.buttons):
            i = x % items_per_row
            button.menu = surface
            button.x = (i+1)*((self.menu_width - items_per_row*(self.button_width+items_per_row))/(items_per_row+1))+(self.button_width+items_per_row)*i
            button.y = text_surface.get_height()+self.button_gap/3 + (self.button_height+self.button_gap)*math.floor(x/items_per_row)
            button.button_width = self.button_width
            button.button_height = self.button_height

            button.drawInSurface(surface)
        

        screen.blit(surface, (self.ori_x,self.ori_y))


    def drawDisplayers(self, screen):
        surface = pygame.Surface((self.menu_width, self.menu_height))
        surface.fill((0,0,0))
        
        
        if self.menu_img != None:
            bg = pygame.transform.scale(self.menu_img,(int(self.menu_width),int(self.menu_height)))
            surface.blit(bg, (0,0))
        elif self.menu_color != None:
            surface.fill(self.menu_color)

        for displayer in self.displayers:
            displayer.drawDisplayers(surface, self.ori_x, self.ori_y)

        screen.blit(surface, (self.ori_x, self.ori_y))










        
