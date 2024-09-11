import math
import pickle
import pygame.image

from src.audio_handler import play_sound
from src.custom_timer import Timer
from src.stopwatch import Stopwatch
from abc import ABC, abstractmethod


class Puzzle(ABC):

    def __init__(self, surface, size_x, size_y, amount, image_path, rotatable):
        self.pieces = {}
        self.rowcols = ()
        self.connected_groups = []
        self.active = None
        self.drag_timer = Timer(200)
        self.click = False
        self.rotatable = rotatable
        self.image_path = image_path
        self.image = pygame.transform.scale(pygame.image.load(image_path), (size_x, size_y))
        piece_dims = self.__set_piece_dims(size_x, size_y, amount)
        self.create_pieces(surface, self.rowcols, piece_dims)
        self.stopwatch = Stopwatch()
        self.save_path = f"{self.image_path}{self.rowcols[0] * self.rowcols[1]}.pkl"

    def get_amount(self):
        return self.rowcols[0] * self.rowcols[1]

    def draw(self, surface, text_col):
        visited_groups = []
        for piece in self.pieces.values():
            group = self.find_group(piece)
            if group is None:
                piece.relocate_inside_surface(surface)
                piece.draw(surface)
            else:
                if group in visited_groups:
                    continue
                all_outside = True
                for grp_piece in group:
                    if grp_piece.is_in_surface(surface):
                        all_outside = False
                        break
                if all_outside:
                    movement_vector = next(iter(group)).relocate_inside_surface(surface)
                    for grp_piece in group:
                        if grp_piece != next(iter(group)):
                            grp_piece.move(movement_vector)
                for grp_piece in group:
                    grp_piece.draw(surface)
                visited_groups.append(group)
        self.draw_stopwatch(surface, text_col)

    def draw_stopwatch(self, surface, text_col):
        font = pygame.font.SysFont("arialblack", 20)
        text = font.render(self.stopwatch.get_elapsed_time(), True, text_col)
        surface.blit(text, (surface.get_width() - 80, 0))

    def pause_stopwatch(self):
        self.stopwatch.pause_toggle()

    def __set_piece_dims(self, width, height, amount):

        def within_ratio(w, h):
            ratio = w / h if w >= h else h / w
            return 0.6 <= ratio <= 1.6

        def factor_pairs(n):
            return [(i, n // i) for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]

        pairs = sorted(factor_pairs(amount), key=lambda x: abs(x[0] - x[1]))

        for factor_w, factor_h in pairs:
            for fw, fh in [(factor_w, factor_h), (factor_h, factor_w)]:
                if within_ratio(width / fw, height / fh):
                    self.rowcols = (fw, fh)
                    return width / fw, height / fh
        raise AttributeError("Invalid square amount")

    @staticmethod
    def get_possible_piece_dims(width, height):
        def within_ratio(w, h):
            ratio = w / h if w >= h else h / w
            return 0.6 <= ratio <= 1.6

        possible_amounts = set()
        max_pieces = 1500

        for i in range(1, int(width) + 1):
            piece_width = width / i
            for j in range(1, int(height) + 1):
                piece_height = height / j
                if within_ratio(piece_width, piece_height):
                    pieces_count = i * j
                    if 1 < pieces_count <= max_pieces:
                        possible_amounts.add(pieces_count)
                    else:
                        break

        return sorted(possible_amounts)

    def find_position(self, piece):
        for position, p in self.pieces.items():
            if p == piece:
                return position
        return None

    def get_piece_image(self, row, col, width, height):
        return self.image.subsurface(pygame.Rect(col * width, row * height, width, height))

    def rotate(self, clockwise):
        if self.active and self.rotatable:
            group = self.find_group(self.active)
            if group:
                for piece in group:
                    piece.rotate(clockwise)
            else:
                self.active.rotate(clockwise)

    def check_collisions(self, piece):
        piece_row, piece_col = self.find_position(piece)
        neighbors = [(piece_row-1, piece_col), (piece_row+1, piece_col),
                     (piece_row, piece_col-1), (piece_row, piece_col+1)]
        piece_group = self.find_group(piece)
        for neighbor_loc in neighbors:
            neighbor = self.pieces.get(neighbor_loc)
            if (neighbor and (piece_group is None or neighbor not in piece_group) and
                    piece.check_collision(neighbor, (neighbor_loc[0] - piece_row, neighbor_loc[1] - piece_col))):
                self.connect_pieces(piece, neighbor, (neighbor_loc[0] - piece_row, neighbor_loc[1] - piece_col))

    def connect_pieces(self, piece1, piece2, rel_pos):
        play_sound("resources/piece_click.mp3")
        group1, group2 = self.find_group(piece1), self.find_group(piece2)
        rel_change = piece1.attach_to_piece(piece2, rel_pos)
        if group1 and group2:
            if group1 != group2:
                for piece in group1:
                    if piece != piece1:
                        piece.move(rel_change)
                group1.update(group2)
                self.connected_groups.remove(group2)
        elif group1:
            for piece in group1:
                if piece != piece1:
                    piece.move(rel_change)
            group1.add(piece2)
        elif group2:
            group2.add(piece1)
        else:
            self.connected_groups.append({piece1, piece2})

    def move(self, rel):
        if self.active:
            self.stopwatch.start()
            group = self.find_group(self.active)
            if group:
                for p in group:
                    p.move(rel)
            else:
                self.active.move(rel)

    def find_group(self, piece):
        for group in self.connected_groups:
            if piece in group:
                return group
        return None

    def handle_click(self, pos):
        if not self.click:  # either click to pickup or drop
            self.click = True
            if not self.active:
                for piece in self.pieces.values():
                    if piece.click(pos):
                        self.active = piece
                        self.drag_timer.start()
                        break
            else:
                group = self.find_group(self.active)
                if group:
                    loop_group = group.copy()
                    for piece in loop_group:
                        self.check_collisions(piece)
                else:
                    self.check_collisions(self.active)
                self.active = None

    def handle_click_stop(self):
        if self.drag_timer.is_time_up():  # dragging is active
            group = self.find_group(self.active)
            if group:
                loop_group = group.copy()
                for piece in loop_group:
                    self.check_collisions(piece)
            else:
                self.check_collisions(self.active)
            self.active = None
        self.drag_timer.stop()
        self.click = False

    def is_complete(self):
        return len(self.connected_groups) == 1 and len(self.connected_groups[0]) == len(self.pieces)

    def save_to_file(self, filename=""):
        if not filename:
            filename = self.save_path
        with open(filename, 'wb') as file:
            pickle.dump(self.serialize(), file)

    @abstractmethod
    def create_pieces(self, surface, rowcols, piece_dim):
        pass

    @staticmethod
    @abstractmethod
    def load(filename, surface):
        pass

    @staticmethod
    def clearsave(filename):
        open(filename, 'w').close()

    @abstractmethod
    def serialize(self):
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data, surface):
        pass
