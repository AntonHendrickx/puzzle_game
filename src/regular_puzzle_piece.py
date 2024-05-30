import pygame
from src.puzzle_piece import piece

class regular_piece(piece):

    def __init__(self, x, y, size_x, size_y):
        super().__init__(x, y)
        self.piece = pygame.Rect(x, y, size_x, size_y)

    def draw(self, surface):
        surface_width, surface_height = surface.get_size()
        if self.piece.left < 0:
            self.piece.left = 0
        if self.piece.right > surface_width:
            self.piece.right = surface_width
        if self.piece.top < 0:
            self.piece.top = 0
        if self.piece.bottom > surface_height:
            self.piece.bottom = surface_height
        pygame.draw.rect(surface, (255,255,255), self.piece)

    def check_collision(self, piece_tocheck):
        pass
