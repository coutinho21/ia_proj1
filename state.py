from enum import Enum

class GameState(Enum):
        MENU = 0
        GAME_MODE_MENU = 1
        PvsP = 2
        PvsAI = 3
        AIvsAI = 4
        RED_WON = 5
        BLUE_WON = 6
        QUIT = 7
        RULES = 8