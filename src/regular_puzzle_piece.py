import pygame
from src.puzzle_piece import Piece


class RegularPiece(Piece):

    def __init__(self, x, y, size_x, size_y, image, rotation=0):
        super().__init__(x, y, image, rotation)
        self.piece = pygame.Rect(x, y, size_x, size_y)
        self.topleft = self.piece.topleft

    def get_width(self):
        return self.piece.width

    def get_height(self):
        return self.piece.height

    def draw(self, surface):
        self.relocate_inside_surface(surface)
        if self.image:
            surface.blit(self.image, self.piece)
        else:
            pygame.draw.rect(surface, (255, 255, 255), self.piece)

    def relocate_inside_surface(self, surface):
        surface_width, surface_height = surface.get_size()
        if self.piece.right < 0:
            self.piece.left = 0
        if self.piece.left > surface_width:
            self.piece.right = surface_width
        if self.piece.bottom < 0:
            self.piece.top = 0
        if self.piece.top > surface_height:
            self.piece.bottom = surface_height

    def is_in_surface(self, surface):
        surface_width, surface_height = surface.get_size()
        in_surface = True
        if self.piece.right < 0:
            in_surface = False
        if self.piece.left > surface_width:
            in_surface = False
        if self.piece.bottom < 0:
            in_surface = False
        if self.piece.top > surface_height:
            in_surface = False
        return in_surface

    def check_collision(self, piece_tocheck, rel_pos, tolerance=10):
        if not super().check_collision(piece_tocheck, rel_pos):
            return False
        expected_x = self.piece.x + rel_pos[1] * self.get_width()
        expected_y = self.piece.y + rel_pos[0] * self.get_height()
        is_close_x = abs(piece_tocheck.piece.x - expected_x) <= tolerance
        is_close_y = abs(piece_tocheck.piece.y - expected_y) <= tolerance
        return is_close_x and is_close_y

    def attach_to_piece(self, p, rel_pos):
        new_x, new_y = p.piece.topleft
        if rel_pos == (1, 0):
            new_y -= p.get_height()
        elif rel_pos == (-1, 0):
            new_y += self.piece.height
        elif rel_pos == (0, -1):
            new_x += self.piece.width
        elif rel_pos == (0, 1):
            new_x -= p.get_width()
        rel_change = (new_x - self.piece.topleft[0], new_y - self.piece.topleft[1])
        self.piece.topleft = (new_x, new_y)
        self.topleft = (new_x, new_y)
        return rel_change

    def rotate(self, clockwise):
        super().rotate(clockwise)
        old_center = self.piece.center
        if clockwise:
            pygame.transform.rotate(self.image, -90)
            self.piece = self.image.get_rect(center=old_center)
        else:
            pygame.transform.rotate(self.image, 90)
            self.piece = self.image.get_rect(center=old_center)

    def serialize(self):
        return {
            'x': self.piece.x,
            'y': self.piece.y,
            'width': self.piece.width,
            'height': self.piece.height,
            'image': pygame.image.tostring(self.image, "ARGB"),
            'rotation': self.direction
        }

    @staticmethod
    def deserialize(data):
        image = pygame.image.fromstring(data['image'], (data['width'], data['height']), "ARGB")
        piece_image = pygame.transform.scale(image, (data['width'], data['height']))
        piece = RegularPiece(data['x'], data['y'], data['width'], data['height'], piece_image, data['rotation'])
        return piece
