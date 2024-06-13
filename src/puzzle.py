import math
import pickle
import pygame.image

from src.custom_timer import Timer
from src.stopwatch import Stopwatch
from abc import ABC, abstractmethod


class Puzzle(ABC):

    def __init__(self, surface, size_x, size_y, amount, image_path, rotatable):
        self.amount = amount
        self.pieces = {}
        self.rowcols = ()
        self.connected_groups = []
        self.active = None
        self.drag_timer = Timer(200)
        self.click = False
        self.rotatable = rotatable
        self.image_path = image_path
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (size_x, size_y))
        piece_dims = self.__set_piece_dims(size_x, size_y, amount)
        self.create_pieces(surface, self.rowcols, piece_dims)
        self.stopwatch = Stopwatch()
        self.save_path = self.image_path + str(self.amount) + ".pkl"

    def draw(self, surface):
        for (_, _), piece in self.pieces.items():
            piece.draw(surface)
        self.draw_stopwatch(surface)

    def draw_stopwatch(self, surface):
        font = pygame.font.SysFont("arialblack", 20)
        text = font.render(self.stopwatch.get_elapsed_time(), True, (255, 255, 255))
        surface.blit(text, (surface.get_width()-80, 0))

    def pause_stopwatch(self):
        self.stopwatch.pause_toggle()

    def __set_piece_dims(self, width, height, amount):

        def within_ratio(w, h):
            ratio = w / h if w >= h else h / w
            return 0.6 <= ratio <= 1.6

        def factor_pairs(n):
            return [(i, n // i) for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]

        rect_ratio = width / height if width >= height else height / width
        pairs = factor_pairs(amount)
        pairs.sort(key=lambda x: abs(x[0] - x[1]))

        for factor_w, factor_h in pairs:
            pair_ratio = factor_w / factor_h if factor_w >= factor_h else factor_h / factor_w
            if (rect_ratio >= 1 and pair_ratio >= 1) or (rect_ratio < 1 and pair_ratio < 1):
                square_width = width / factor_w
                square_width_2 = width / factor_h
                square_height = height / factor_h
                square_height_2 = height / factor_w

                if within_ratio(square_width, square_height):
                    self.rowcols = (factor_w, factor_h)
                    return square_width, square_height
                elif within_ratio(square_width_2, square_height_2):
                    self.rowcols = (factor_h, factor_w)
                    return square_width_2, square_height_2
        raise AttributeError("Invalid square amount")

    @staticmethod
    def get_possible_piece_dims(width, height):
        def within_ratio(w, h):
            ratio = w / h if w >= h else h / w
            return 0.6 <= ratio <= 1.6

        possible_amounts = []
        max_pieces = 1500

        for i in range(1, int(width) + 1):
            for j in range(1, int(height) + 1):
                piece_width = width / i
                piece_height = height / j

                if within_ratio(piece_width, piece_height):
                    pieces_count = i * j
                    if 1 < pieces_count <= max_pieces:
                        possible_amounts.append(pieces_count)
                    else:
                        break

        return sorted(set(possible_amounts))

    @abstractmethod
    def create_pieces(self, surface, rowcols, piece_dim):
        pass

    def find_position(self, piece):
        key_list = list(self.pieces.keys())
        val_list = list(self.pieces.values())
        return key_list[val_list.index(piece)]

    def get_piece_image(self, row, col, width, height):
        x = col * width
        y = row * height
        return self.image.subsurface(pygame.Rect(x, y, width, height))

    def rotate(self, clockwise):
        if self.active and self.rotatable:
            self.active.rotate(clockwise)

    def check_collisions(self, piece):
        piece_row, piece_col = self.find_position(piece)
        neighbors = [(piece_row-1, piece_col), (piece_row+1, piece_col),
                     (piece_row, piece_col-1), (piece_row, piece_col+1)]
        for neighbor_loc in neighbors:
            neighbor = self.pieces.get(neighbor_loc)
            if neighbor:
                rel_pos = neighbor_loc[0] - piece_row, neighbor_loc[1] - piece_col
                if piece.check_collision(neighbor, rel_pos):
                    self.connect_pieces(piece, neighbor, rel_pos)

    def connect_pieces(self, piece1, piece2, rel_pos):
        group1 = self.find_group(piece1)
        group2 = self.find_group(piece2)
        piece1.set_position(piece2, rel_pos)
        if group1 is not None and group2 is not None:
            if group1 != group2:
                group1.update(group2)
                self.connected_groups.remove(group2)
        elif group1 is not None:
            group1.add(piece2)
        elif group2 is not None:
            group2.add(piece1)
        else:
            new_group = {piece1, piece2}
            self.connected_groups.append(new_group)

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
                for (_, _), piece in self.pieces.items():
                    if piece.click(pos):
                        self.active = piece
                        self.drag_timer.start()
                        break
            else:
                self.check_collisions(self.active)
                self.active = None

    def handle_click_stop(self):
        if self.drag_timer.is_time_up():  # dragging is active
            self.check_collisions(self.active)
            self.active = None
        self.drag_timer.stop()
        self.click = False

    def is_complete(self):
        total_pieces = len(self.pieces)
        if len(self.connected_groups) == 1 and len(self.connected_groups[0]) == total_pieces:
            return True
        return False

    def save_to_file(self, filename=""):
        if filename == "":
            filename = self.save_path
        with open(filename, 'wb') as file:
            pickle.dump(self.serialize(), file)

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
