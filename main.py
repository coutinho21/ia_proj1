import pygame
from math import *
from object import Object
from hexagon import Hexagon

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pi2 = 2 * 3.14


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)




radius = 45
width = sqrt(3) * (radius)
height = 2 * radius
hexagons = []

def drawBoard():
        temp = 0
        
        for j in range(5,9):
            for i in range(j):
                hexagons.append(Hexagon(screen, "black", radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height)))
            temp += 1
        for j in range(9, 4, -1):
            for i in range(j):
                hexagons.append(Hexagon(screen, "black", radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height)))
            temp += 1
        for i in range(len(hexagons)):
            hexagons[i].draw(hexagons[i].Surface ,hexagons[i].color, hexagons[i].radius, hexagons[i].position)
            font = pygame.font.Font(None, 15)
            text = font.render(str(i+1), 1, (10, 10, 10))
            hexagons[i].Surface.blit(text, (hexagons[i].position[0] - 15, hexagons[i].position[1] - 15))
        hexagons.clear()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((220,190,131))
    drawBoard()

    # linha a meio do ecra
    # pygame.draw.line(screen, "green", (0,screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()