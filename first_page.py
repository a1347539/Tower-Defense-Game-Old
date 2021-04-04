import pygame
import os
import in_game
import upgradetable
from menuFolder.menu import menu
from playerFolder.players import player
from playerFolder.players import init_user


pygame.init()
pygame.font.init()

start_menu_button_width = 150
start_menu_button_height = 75
gap = 10
start_img = pygame.image.load(os.path.join(
                "img/main_page_img","start_button.png"))

upgrade_img = pygame.image.load(os.path.join(
                "img/main_page_img","upgrade_button.png"))


gold_img = pygame.image.load(os.path.join("img/inGame_topBar","gold.png"))

class firstPage:
    def __init__(self, screen_width, screen_height, current_player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.main_page_bg = pygame.transform.scale(
            pygame.image.load(os.path.join(
                "img","main_page_bg.jpg")),(self.screen_width, self.screen_height))
        
        self.clock = pygame.time.Clock()
        self.current_player = current_player
        
        self.start = True
        self.currentSelected = None

        self.start_menu_item = [(start_img, "start", None, None), (upgrade_img, "upgrade", None, None)]
        self.start_menu = menu((self.screen_width-start_menu_button_width)/2, (self.screen_height-start_menu_button_height)/2,
                               start_menu_button_width, (start_menu_button_height + gap) * len(self.start_menu_item),self.start_menu_item, None, None,
                               None, None, None, 
                               start_menu_button_width, start_menu_button_height, gap,
                               None, None)
        
    def run(self):
        self.screen.blit(self.main_page_bg, (0,0))
        
        while self.start:
            self.clock.tick(20)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_pos = pygame.mouse.get_pos()
                    if self.cursor_in_range(cursor_pos, self.start_menu):
                        for button in self.start_menu.buttons:
                            if button.click(cursor_pos[0], cursor_pos[1]) == "start":
                                #self.fade_out()
                                return "start"
                            elif button.click(cursor_pos[0], cursor_pos[1]) == "upgrade":
                                UT = upgradetable.upgrade_table(self.screen, self.screen_width, self.screen_height, self.current_player)
                                UT.run()


            self.draw(self.screen)

            pygame.display.flip()
        pygame.quit()


    def draw(self, screen):
        
        self.screen.blit(self.main_page_bg, (0,0))
        self.start_menu.draw_vertical(screen)
        self.drawTopBar(screen, self.screen_width, self.screen_height)

    def cursor_in_range(self, cursor, obj):
        if obj.x < cursor[0] < obj.x + obj.menu_width:
            if obj.y < cursor[1] < obj.y + obj.menu_height:
                return True
        return False

    def drawTopBar(self, screen, screen_width, screen_height):
        button_length = screen_height/22
        txt_length = button_length * 4
        topBar_menu_item = [(gold_img, int(self.current_player.money), None, (191, 145, 17))]
        topBar_menu = menu((1/2)*screen_width, 0,
                           screen_width/2, screen_height/11, topBar_menu_item, None, None,
                           int(button_length) + txt_length, int(button_length), 0.6,
                           int(button_length), int(button_length), (screen_width/2 - (len(topBar_menu_item) * (int(button_length) + txt_length))) / (len(topBar_menu_item) + 1),
                           txt_length, (255, 255, 255),
                           )
        topBar_menu.drawMenuWithTxt(screen)

    def fade_out(self): 
        fade_surface = pygame.Surface((self.screen_width, self.screen_height))
        fade_surface.fill((0,0,0))
        for alpha in range(0, 300):
            fade_surface.set_alpha(alpha)
            self.draw(self.screen)
            self.screen.blit(fade_surface, (0,0))
            pygame.display.update()












        
