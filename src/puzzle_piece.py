import pygame
from abc import ABC, abstractmethod

class piece(ABC):
    def __init__(self, x, y):
        self.topleft = (x,y)
        self.piece = None
        self.drag = False
        self.clicked = False

    @abstractmethod
    def draw(self, surface):
        pos = pygame.mouse.get_pos()

        if self.piece.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.drag = not self.drag
            self.clicked = False

    def move_piece(self, rel):
        pos = pygame.mouse.get_pos()
        if self.drag and self.piece.collidepoint(pos):
            self.piece.move_ip(rel)
        else:
            self.drag = False

    def draggable(self, draggable):
        self.drag = draggable
