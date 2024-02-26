
class Object:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.color = (255, 0, 0)  # Red color by default


    def move(self, dx, dy):
        self.x += dx
        self.y += dy