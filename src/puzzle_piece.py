from abc import ABC, abstractmethod

class piece(ABC):
    def __init__(self, x, y):
        self.topleft = (x,y)
        self.piece = None
        self.clicked = False
        self.direction = "up"

    @abstractmethod
    def draw(self, surface):
        pass

    def move(self, rel):
        self.piece.move_ip(rel)

    def click(self,pos):
        return self.piece.collidepoint(pos)

    @abstractmethod
    def check_collision(self, piece_tocheck):
        return piece_tocheck.direction == self.direction