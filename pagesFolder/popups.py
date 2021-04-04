import pygame
from menusFolder import menu

class button:
    def __init__(self, button_img, button_obj):
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.button_img = button_img
        self.button_obj = button_obj
        
    def draw(self):
        pass


    def click(self, cursor_x, cursor_y):
        if self.x <= cursor_x <= self.x + self.width:
            if self.y <= cursor_y <= self.y + self.height:
                return self.button_obj
    
class displayer:

    def __init__(self, x, y, width, height, img, color, displayer_items, Type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.color = color
        self.displayer_items = displayer_items
        self.Type = Type
        self.surface = pygame.Surface((self.width,self.height))
        self.buttons = []

        if self.Type == "b":
            for displayer_item in self.displayer_items:
                self.buttons.append(button(displayer_item[0], displayer_item[1]))

    def draw(self, popup):
        if self.color != None:
            self.surface.fill(self.color)
                
        if self.Type == "m":
            img = pygame.transform.scale(self.obj, (int(self.width), int(self.height)))
            self.surface.blit(img, (0,0))
            
        if self.Type == "b":
            for button in self.buttons:
                button.x = self.x
                button.y = self.y
                button.width = self.width
                button.height = self.height
        
        popup.blit(self.surface, (self.x, self.y))

    def init(self):
        pass        
        
class popup:
    def __init__(self, x, y,
                 popup_width, popup_height,
                 popup_items, popup_img, popup_color,
                 ):
        
        self.x = x
        self.y = y
        self.popup_width = popup_width
        self.popup_height = popup_height
        self.popup_items = popup_items
        self.popup_img = popup_img
        self.popup_color = popup_color
        self.displayers = []

        for surface in self.popup_items:
            self.displayers.append(menu(surface[0],surface[1],
                                        surface[2],surface[3],
                                        surface[4],surface[5],
                                        surface[6],surface[7]
                                        ))

    def draw(self, screen):
        surface = pygame.Surface((self.popup_width, self.popup_height))
        
        if self.popup_img != None:
            bg = pygame.transform.scale(self.popup_img,(int(self.popup_width),int(self.popup_height)))
            surface.blit(bg, (0,0))
        elif self.popup_color != None:
            surface.fill(self.popup_color)

        for displayer in self.displayers:
            displayer.draw(surface)

        screen.blit(surface, (self.x, self.y))
        
    def onChange(self, screen):
        pygame.screen.fill(0,0,0)
