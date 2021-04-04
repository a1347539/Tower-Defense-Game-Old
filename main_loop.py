import pygame
import os
import first_page
import in_game
import prep_page

import time

from playerFolder.players import player
from playerFolder.players import init_user


pygame.init()
pygame.font.init()

start_img = pygame.transform.scale(
            pygame.image.load(os.path.join(
                "img/main_page_img","start_button.png")),(20, 20))


class main_game:
    def __init__(self, player):
        self.screen_width = 700
        self.screen_height = 500
        self.clock = pygame.time.Clock()

        self.current_player = player
        #print(self.current_player.towers_upgrades)
        
#for firstPage
        self.inFirstPage = True

#for inGame
        self.inGame = False
        self.current_level = None
        self.current_towers = None

        self.start = True
        
#for pre_page
        self.inPreGame = False

        
    def run(self):
        
        while self.start:
            self.clock.tick(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False

            if self.inFirstPage:
                firstpage = first_page.firstPage(self.screen_width, self.screen_height, self.current_player)
                if firstpage.run() == "start":
                    self.inFirstPage = False
                    self.inPreGame = True
                    
            elif self.inPreGame:
                PreGame = prep_page.prepPage(self.screen_width, self.screen_height, self.current_player)
                v = PreGame.run()
                if v == "e":
                    self.inPreGame = False
                    self.inFirstPage = True
                else:
                    self.current_level = v[0]()
                    self.current_towers = v[1]

                
                    self.inPreGame = False
                    self.inGame = True
                    

            elif self.inGame:
                new_game = in_game.game(self.screen_width, self.screen_height, self.current_player)
                new_game.current_level = self.current_level
                new_game.towers_id = self.current_towers
                result = new_game.run()
                self.current_player.money += result
                self.inGame = False
                self.inFirstPage = True


                
            pygame.display.update()
        pygame.quit()


    def loading_screen(self):
        self.screen.blit(self.loading_img, (0,0))



if __name__ == "__main__":
    data = init_user()
    player = player(data)
    g = main_game(player)
    g.run()



