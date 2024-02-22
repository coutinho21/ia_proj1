import pygame
import sys
from math import *
from object import Object

class Hexagon(Object) :
    

    def __init__(self, Surface, color, radius, position):
        super().__init__(position)
        self.color = color
        self.radius = radius
        self.Surface = Surface
        self.position = position

    def draw(self, Surface, color, radius, position):
        pi2 = 2 * 3.14
        pygame.draw.lines(Surface,
                color,
                True,
                [(sin(i / 6 * pi2) * radius + position[0], cos(i / 6 * pi2) * radius + position[1]) for i in range(0, 6)])


        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy