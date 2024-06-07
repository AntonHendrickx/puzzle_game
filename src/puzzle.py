import math
import pickle
import random
import pygame.image
from src.regular_puzzle_piece import RegularPiece
from src.timer import Timer


class Puzzle:

    # use image later instead of rect
    def __init__(self, surface, size_x, size_y, amount, image_path, rotatable):
        self.amount = amount
        self.pieces = {}
        self.amounts = ()
        self.connected_groups = []
        self.active = None
        self.drag_timer = Timer(200)
        self.click = False
        self.rotatable = rotatable
        self.image_path = image_path
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (size_x, size_y))
        piece_dims = self.__set_piece_dims(size_x, size_y, amount)
        self.create_pieces(surface, self.amounts, piece_dims)

    def draw(self, surface):
        for (_, _), piece in self.pieces.items():
            piece.draw(surface)

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
                    self.amounts = (factor_w, factor_h)
                    return square_width, square_height
                elif within_ratio(square_width_2, square_height_2):
                    self.amounts = (factor_h, factor_w)
                    return square_width_2, square_height_2
        raise AttributeError("Invalid square amount")

    def create_pieces(self, surface, amounts, piece_dim):
        piece_width, piece_height = piece_dim
        cols, rows = amounts
        screen_width, screen_height = surface.get_size()

        for row in range(rows):
            for col in range(cols):
                rotation = 0
                x = random.randint(0, int(screen_width - piece_width))
                y = random.randint(0, int(screen_height - piece_height))
                piece_image = self.get_piece_image(row, col, piece_width, piece_height)
                if self.rotatable:
                    rotation = random.randint(0, 3)
                self.pieces[(row, col)] = RegularPiece(x, y, piece_width, piece_height, piece_image, rotation)

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
            filename = "saves/" + self.image_path.replace("images/", "") + ".pkl"
        with open(filename, 'wb') as file:
            pickle.dump(self.serialize(), file)

    @staticmethod
    def load(filename, surface):
        try:
            with open(filename, 'rb') as file:
                obj = pickle.load(file)
                puzzle_found = Puzzle.deserialize(obj, surface)
                if isinstance(puzzle_found, Puzzle):
                    return puzzle_found
                else:
                    return None
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, KeyError, FileNotFoundError):
            return None

    @staticmethod
    def clearsave(filename):
        open(filename, 'w').close()

    def serialize(self):
        return {
            'size_x': self.image.get_width(),
            'size_y': self.image.get_height(),
            'amount': self.amount,
            'amounts': self.amounts,
            'pieces': {key: piece.serialize() for key, piece in self.pieces.items()},
            'connected_groups': [[self.find_position(p) for p in group] for group in self.connected_groups],
            'active': self.find_position(self.active) if self.active else None,
            'rotatable': self.rotatable,
            'image_path': self.image_path
        }

    @staticmethod
    def deserialize(data, surface):
        puzzle = Puzzle(surface, data['size_x'], data['size_y'], data['amount'], data['image_path'], data['rotatable'])
        puzzle.amounts = data['amounts']
        puzzle.pieces = {key: RegularPiece.deserialize(piece_data) for key, piece_data in data['pieces'].items()}
        puzzle.connected_groups = [{puzzle.pieces[pos] for pos in group} for group in data['connected_groups']]
        puzzle.active = puzzle.pieces[data['active']] if data['active'] else None
        return puzzle
