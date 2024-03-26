from math import cos, sin, sqrt
import pygame
from object import Object
from utils import drawText

class Button(Object):
    def __init__(self, position, color, text, size, action, text_size = 25, shape = 'rect'):
        super().__init__(position)
        self.color = color
        self.text = text
        self.size = size
        self.action = action
        self.text_size = text_size
        self.shape = shape

    def draw(self, screen, color=(220,190,131)):
        if self.shape == 'rect':
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size[0], self.size[1]))
            drawText(screen, self.text, 'black', self.text_size, self.x + self.size[0] / 2, self.y + self.size[1] / 2)
        if self.shape == 'hexagon':
            pi2 = 2 * 3.14
            points = [(sin(i / 6 * pi2) * self.size[0] + self.x, cos(i / 6 * pi2) * self.size[1] + self.y) for i in range(0, 6)]
            mouse_pos = pygame.mouse.get_pos()
            hexagon_rect = pygame.draw.polygon(screen, color, points)
            pygame.draw.lines(screen, self.color, True, points,3)

            if hexagon_rect.collidepoint(mouse_pos):
                pygame.draw.polygon(screen, self.color, points)

            drawText(screen, self.text, 'black', self.text_size, self.x , self.y )

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.shape == 'rect':
            return self.x <= pos[0] <= self.x + self.size[0] and self.y <= pos[1] <= self.y + self.size[1]
        if self.shape == 'hexagon':
            distance = sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)
            return distance <= self.size[0] 