from enum import Enum

class GameState(Enum):
        MENU = 0
        PvsP = 1
        PvsAI = 2
        AIvsAI = 3
        RED_WON = 2
        BLUE_WON = 3
        QUIT = 4
        RULES = 5