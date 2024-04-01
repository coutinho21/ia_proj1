import pygame
from math import *
from object import Object

class Hexagon(Object) :
    def __init__(self, Surface, color, radius, position,pos_n, base = None):
        super().__init__(position)
        self.color = color
        self.radius = radius
        self.Surface = Surface
        self.position = position
        self.pos_n = pos_n
        self.base = base


    def draw(self, Surface, color, radius, position):
        pi2 = 2 * 3.14
        pygame.draw.lines(Surface,
                color,
                True,
                [(sin(i / 6 * pi2) * radius + position[0], cos(i / 6 * pi2) * radius + position[1]) for i in range(0, 6)])
        if(self.base != None):
            pygame.draw.circle(Surface, self.base, (int(position[0]), int(position[1])), 16, 0)


    def distance_to(self, piece):
        if piece is None:
            return None
        # Calculate the distance between the hexagon's center and the piece's center
        return sqrt((self.position.x - piece.position.x) ** 2 + (self.position.y - piece.position.y) ** 2)


    def is_clicked(self):
        pos = pygame.mouse.get_pos()
    # Calculate the Euclidean distance between the piece's center and the mouse position
        distance = sqrt((self.position.x - pos[0]) ** 2 + (self.position.y - pos[1]) ** 2)
    
    # If the distance is less than the radius, the mouse click is inside the piece
        return distance <= self.radius