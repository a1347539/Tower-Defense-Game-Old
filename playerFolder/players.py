import json
from os import path

def init_user():
    blank_data = {
        'player_id': {
            'Id': None,
            'pw': None,
        }
        ,
        'player_game_data': {
            'money': 10000,
            
        }
        ,
        'general_upgrades': {
            
            'tower_slots': [1,[20,40,70,90,200,400]],
            'damage': [1,[20,40,70,90,100,140,400,700,800,1600]],
            'range': [1,[20,40,70,90,100,140,400,700,800,1600]],
            'effect': [1,[20,40,70,90,100,140,400,700,800,1600]],
            'attack_speed': [1,[20,40,70,90,100,140,400,700,800,1600]],
            'idle': [1,[0]],
            'idle1': [1,[0]]

        }
        ,
        'towers_upgrade': {
            '1': {
                'unlocked': [False, 70],
                'damage': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'range': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'effect': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'attack_speed': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'idle': [1,[0]],
                'idle1': [1,[0]]
                },
            '2': {
                'unlocked': [False, 70],
                'damage': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'range': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'effect': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'attack_speed': [1,[20,40,70,90,100,140,400,700,800,1600]],
                'idle': [1,[0]],
                'idle1': [1,[0]]
                }
        }
    }
    if path.exists('playerFolder/playerdata/user.txt'):
        with open('playerFolder/playerdata/user.txt') as infile:
            infile = json.load(infile)
            return infile
    else:
        json_object = json.dumps(blank_data, indent = 4)
        with open('playerFolder/playerdata/user.txt', 'w') as outfile:
            outfile.write(json_object)
        return blank_data




class player:
    def __init__(self, data):
        
        self.Id = data['player_id']['Id']
        self.pw = data['player_id']['pw']
        
        self.money = data['player_game_data']['money']

        self.general_upgrades = data['general_upgrades']

        self.towers_upgrades = data["towers_upgrade"]

        #print(self.towers_upgrades["1"]['unlocked'])

