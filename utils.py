import pygame

def drawText(screen, inputText, color, fontSize, x, y):
    font = pygame.font.Font(None, fontSize)
    text = font.render(inputText, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)