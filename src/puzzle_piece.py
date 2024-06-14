from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, x, y, image, direction=0):
        self.DIRECTIONS = ["up", "right", "down", "left"]
        self.topleft = (x, y)
        self.piece = None
        self.clicked = False
        self.direction = direction
        self.image = image

    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def move(self, rel):
        self.piece.move_ip(rel)

    def click(self, pos):
        return self.piece.collidepoint(pos)

    def get_dir(self):
        return self.DIRECTIONS[self.direction]

    @abstractmethod
    def rotate(self, clockwise):
        if clockwise:
            self.direction += 1
        else:
            self.direction -= 1

    @abstractmethod
    def check_collision(self, piece_tocheck, rel_pos):
        return piece_tocheck.get_dir() == self.get_dir()

    @abstractmethod
    def attach_to_piece(self, p, rel_pos):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def relocate_inside_surface(self, surface):
        pass

    @abstractmethod
    def is_in_surface(self, surface):
        pass

    @staticmethod
    @abstractmethod
    def deserialize(self):
        pass
