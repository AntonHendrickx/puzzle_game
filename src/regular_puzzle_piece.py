import pygame
from src.puzzle_piece import piece

class regular_piece(piece):

    def __init__(self, x, y, size_x, size_y):
        super().__init__(x, y)
        self.piece = pygame.Rect(x, y, size_x, size_y)

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.rect(surface, (255,255,255), self.piece)

    def check_collision(self, piece_tocheck):
        pass
