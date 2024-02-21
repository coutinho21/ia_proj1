import pygame
from math import *
from object import Object

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
test =  Object(100, 100)
running = True
dt = 0
pi2 = 2 * 3.14


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def draw_hexagon(Surface, color, radius, position):
    print([(sin(i / 6 * pi2) * radius + position[0], cos(i / 6 * pi2) * radius + position[1]) for i in range(0, 6)])
    return pygame.draw.lines(Surface,
          color,
          True,
          [(sin(i / 6 * pi2) * radius + position[0], cos(i / 6 * pi2) * radius + position[1]) for i in range(0, 6)])


width = 61
height = 70

def drawBoard():
        test.draw(screen)
        temp = 0
        for j in range(5,9):
            for i in range(j):
                draw_hexagon(screen, "black", 35, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height))
            temp += 1
        for j in range(9, 4, -1):
            for i in range(j):
                draw_hexagon(screen, "black", 35, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height))
            temp += 1
             


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