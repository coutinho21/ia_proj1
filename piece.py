import pygame
import sys
from object import Object

class Piece(Object) :
    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.color = color
        self.radius = 35

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy