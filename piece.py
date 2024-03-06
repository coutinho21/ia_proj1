from math import sqrt
import pygame
from object import Object
from utils import drawText

class Piece(Object) :
    def __init__(self, position, color, pos_n, selected = False, isBlocked = False):
        super().__init__(position)
        self.color = color
        self.radius = 25
        self.position = position
        self.pos_n = pos_n
        self.selected = selected
        self.isBlocked = isBlocked


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        if self.isBlocked:
            drawText(screen, 'Blocked', (0, 0, 0), 14, self.position[0], self.position[1])


    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        
        # Calculate the Euclidean distance between the piece's center and the mouse position
        distance = sqrt((self.position.x - pos[0]) ** 2 + (self.position.y - pos[1]) ** 2)

        # If the distance is less than the radius, the mouse click is inside the piece
        return distance <= self.radius


    def move(self, pos_to, position_to):
        self.position = position_to
        self.pos_n = pos_to
