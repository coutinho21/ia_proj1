from math import sqrt
import pygame
import sys
from object import Object

class Piece(Object) :
    def __init__(self, position, color, pos_n, selected = False):
        super().__init__(position)
        self.color = color
        self.radius = 25
        self.position = position
        self.pos_n = pos_n
        self.selected = selected

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
    # Calculate the Euclidean distance between the piece's center and the mouse position
        distance = sqrt((self.position.x - pos[0]) ** 2 + (self.position.y - pos[1]) ** 2)
    
    # If the distance is less than the radius, the mouse click is inside the piece
        return distance <= self.radius
    
    def move(self, position):
        position = position
