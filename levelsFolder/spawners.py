import time

class spawner:
    def __init__ (self, wave_items, path, current_level_Map, tileWidth, tileHieght):
        self.wave_items = wave_items
        self.path = path
        self.current_level_Map = current_level_Map
        self.spawn_speed = self.wave_items[1]
        self.tileWidth = tileWidth
        self.tileHeight = tileHieght

        self.spawn_timer = time.time()

        self.enemy = []
        self.enemyAmount = []
        self.spawnSpeed = wave_items[1]

        self.iter = 0

        self.fps_multiplier = 1
        
        self.allSpawned = False
        
        for enemy, enemyAmount in self.wave_items[0].items():
            self.enemy.append(enemy)
            self.enemyAmount.append(enemyAmount)


    def spawn(self, enemies):
        if self.enemyAmount[self.iter] > 0:
            if time.time() - self.spawn_timer >= 1/(self.fps_multiplier*self.spawn_speed):
                enemies.append(self.enemy[self.iter](self.path, self.current_level_Map, self.tileWidth, self.tileHeight))
                self.enemyAmount[self.iter] -= 1
                self.spawn_timer = time.time()

        else:
            self.iter += 1
            if self.iter == len(self.enemy):
                return True

                
