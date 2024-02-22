import pygame
import sys
from object import Object

class Piece(Object) :
    def __init__(self, position, color):
        super().__init__(position)
        self.color = color
        self.radius = 25
        self.position = position

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

