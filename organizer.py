'''
Rudimentary screenshot organizer to help me sort my uncompressed copies of Steam screenshots
'''

import os

known_games = {
    '429660': 'Tales of Berseria',
    '244850': 'Space Engineers',
    '363600': 'Holy Potatoes A Weapon Shop',
    '13481167430323535872': 'Super Mario RPG',
    '12653426811753988096': 'Super Paper Mario',
    '9943473048373952512': 'Shin Megami Tensei Persona 3 FES'
}

def get_gameid(file):
    parts = file.split('_')
    if len(parts) > 0:
        return parts[0]
    return None


def is_known_game_screenshot(file):
    if get_gameid(file) in known_games:
        return True
    return False

files = [f for f in os.listdir('.') if os.path.isfile(f) and is_known_game_screenshot(f)]

for f in files:
    # do something
    print f
    game_title = known_games[get_gameid(f)]
    if not os.path.exists(game_title):
        os.makedirs(game_title)
    
    os.rename(f, os.path.join(game_title, f))

