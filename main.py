import pygame
from math import *
from object import Object
from hexagon import Hexagon
from piece import Piece

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
blue_pieces = []
red_pieces = []

def initBoard():
    temp = 0
    counter = 0
    for j in range(5,9):
        for i in range(j):
            hexagons.append(Hexagon(screen, "black", radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height),counter))
            counter += 1
        temp += 1
    for j in range(9, 4, -1):
        for i in range(j):
            hexagons.append(Hexagon(screen, "black", radius, pygame.Vector2(screen.get_width() / 2 + width*i - width * (j/2 - 0.5), screen.get_height() / 2 + ((height/4)*3)*temp - 3 * height),counter))
            counter += 1
        temp += 1
    

def drawBoard():
        for i in range(len(hexagons)):
            if(i == 26) : 
                hexagons[i].base = "red"
            if(i == 34) :
                hexagons[i].base = "blue"
            hexagons[i].draw(hexagons[i].Surface ,hexagons[i].color, hexagons[i].radius, hexagons[i].position)
            font = pygame.font.Font(None, 15)
            text = font.render(str(i+1), 1, (10, 10, 10))
            hexagons[i].Surface.blit(text, (hexagons[i].position[0] - 27, hexagons[i].position[1] - 27))



def piecesInit():
    i1 = 0
    j1 = 4
    k1 = 5
    i2 = 35
    j2 = 42
    k2 = 8
    while i1 < 19 and j1 < 26:
        blue_pieces.append(Piece(hexagons[i1].position, 'blue', i1))
        red_pieces.append(Piece(hexagons[j1].position, 'red', j1))
        i1 += k1
        j1 += k1 + 1
        k1 += 1
    blue_pieces.append(Piece(hexagons[27].position, 'blue',27))
    red_pieces.append(Piece(hexagons[33].position, 'red',33))
    
    while i2 < 57 and j2 < 61:
        blue_pieces.append(Piece(hexagons[i2].position, 'blue', i2))
        red_pieces.append(Piece(hexagons[j2].position, 'red', j2))
        i2 += k2
        j2 += k2 - 1
        k2 -= 1
    
        


def drawPieces():
    for j in range(len(blue_pieces)):
        Piece.draw(blue_pieces[j],screen)
    for i in range(len(red_pieces)):
        Piece.draw(red_pieces[i],screen)
   
def getNearByHexagons(piece):
    nearby_hexagons = []
    for hexagon in hexagons:
        if (hexagon.distance_to(piece) <= 2 * radius) and (hexagon.pos_n != piece.pos_n):
            nearby_hexagons.append(hexagon)
    return nearby_hexagons

def movePiece(piece, nearby_hexagons, same_color_p):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                check = False
                for hexagon in nearby_hexagons:
                    if hexagon.is_clicked():
                        check = True
                        for p in same_color_p:
                            if p.pos_n == hexagon.pos_n:
                                print("There is already a piece in that position")
                                return
                            if hexagon.base != None:
                                print("There is a base in that position")
                                return
                        print(f"Moving piece from {piece.pos_n} to {hexagon.pos_n}")
                        Piece.move(piece, hexagon.pos_n, hexagon.position)
                        return
                if check == False:
                    print("Else was clicked")
                    return
                break
            

initBoard()
piecesInit()



while running:

    screen.fill((220,190,131))
    drawBoard()
    drawPieces()

    # linha a meio do ecra
    # pygame.draw.line(screen, "green", (0,screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any blue piece was clicked
            for piece in blue_pieces:
                if piece.is_clicked():
                    nearby_hexagons = getNearByHexagons(piece)
                    movePiece(piece, nearby_hexagons, blue_pieces)

            # Check if any red piece was clicked
            for piece in red_pieces:
                if piece.is_clicked():
                    nearby_hexagons = getNearByHexagons(piece)
                    movePiece(piece, nearby_hexagons, red_pieces)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()