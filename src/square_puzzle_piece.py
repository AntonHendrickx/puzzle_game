import pygame
from src.puzzle_piece import piece

class square_piece(piece):

    def __init__(self, x, y, size_x, size_y,image, rotation = 0):
        super().__init__(x, y,image, rotation)
        self.piece = pygame.Rect(x, y, size_x, size_y)
        self.topleft = self.piece.topleft

    def get_width(self):
        return self.piece.width

    def get_height(self):
        return self.piece.height

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
        if self.image:
            surface.blit(self.image, self.piece)
        else:
            pygame.draw.rect(surface, (255,255,255), self.piece)

    def check_collision(self, piece_tocheck, rel_pos, tolerance = 10):
        if not super().check_collision(piece_tocheck, rel_pos):
            return False
        expected_x = self.piece.x + rel_pos[1] * self.get_width()
        expected_y = self.piece.y + rel_pos[0] * self.get_height()
        is_close_x = abs(piece_tocheck.piece.x - expected_x) <= tolerance
        is_close_y = abs(piece_tocheck.piece.y - expected_y) <= tolerance
        return is_close_x and is_close_y

    def set_position(self, p, rel_pos):
        new_x, new_y = p.piece.topleft
        if rel_pos == (1, 0):
            new_y += p.get_height()
        elif rel_pos == (-1, 0):
            new_y -= self.piece.height
        elif rel_pos == (0, -1):
            new_x -= self.piece.width
        elif rel_pos == (0, 1):
            new_x += p.get_width()
        self.piece.topleft = (new_x, new_y)
        self.topleft = (new_x, new_y)

    def rotate(self, clockwise):
        super().rotate(clockwise)
        old_center = self.piece.center
        if clockwise:
            pygame.transform.rotate(self.image, -90)
            self.piece = self.image.get_rect(center=old_center)
        else:
            pygame.transform.rotate(self.image, 90)
            self.piece = self.image.get_rect(center=old_center)
