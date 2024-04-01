import pygame

def drawText(screen, inputText, color, fontSize, x, y):
    font = pygame.font.Font(None, fontSize)
    text = font.render(inputText, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    

def getDistance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

