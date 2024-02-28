from enum import Enum

class GameState(Enum):
        MENU = 0
        PLAYING = 1
        RED_WON = 2
        BLUE_WON = 3
        QUIT = 4