import pickle
import random
from src.puzzle import Puzzle
from src.regular_puzzle_piece import RegularPiece


class RegularPuzzle(Puzzle):

    def create_pieces(self, surface, rowcols, piece_dim):
        piece_width, piece_height = piece_dim
        cols, rows = rowcols
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
        self.assign_tabs()

    def assign_tabs(self):
        """
        TABS: 0 means flat edge
        1+6 are a tab family, so is 2 and 5 and 3 and 4
        each piece gets a map: {top = x, left = x, right = x, bottom = x}
        """
        max_x = max(self.pieces, key=lambda pos: pos[0])[0]
        max_y = max(self.pieces, key=lambda pos: pos[1])[1]

        for (x, y), piece in self.pieces.items():
            tabs = {'top': 0 if y == 0 else None, 'left': 0 if x == 0 else None, 'right': 0 if x == max_x else None,
                    'bottom': 0 if y == max_y else None}

            if tabs['left'] is None and (x - 1, y) in self.pieces:
                left_neighbor = self.pieces[(x - 1, y)]
                tabs['left'] = 7 - left_neighbor.tabs['right']
            if tabs['top'] is None and (x, y - 1) in self.pieces:
                top_neighbor = self.pieces[(x, y - 1)]
                tabs['top'] = 7 - top_neighbor.tabs['bottom']
            if tabs['right'] is None:
                tabs['right'] = random.randint(1, 6)
            if tabs['bottom'] is None:
                tabs['bottom'] = random.randint(1, 6)

            if (x + 1, y) in self.pieces:
                right_neighbor = self.pieces[(x + 1, y)]
                right_neighbor.tabs['left'] = 7 - tabs['right']
            if (x, y + 1) in self.pieces:
                bottom_neighbor = self.pieces[(x, y + 1)]
                bottom_neighbor.tabs['top'] = 7 - tabs['bottom']
            piece.add_tabs(tabs)

    def serialize(self):
        return {
            'type': 'regular',
            'size_x': self.image.get_width(),
            'size_y': self.image.get_height(),
            'amount': self.get_amount(),
            'rowcols': self.rowcols,
            'pieces': {key: piece.serialize() for key, piece in self.pieces.items()},
            'connected_groups': [[self.find_position(p) for p in group] for group in self.connected_groups],
            'active': self.find_position(self.active) if self.active else None,
            'rotatable': self.rotatable,
            'image_path': self.image_path,
            'stopwatch_time': self.stopwatch.elapsed_time,
            'save_path': self.save_path
        }

    @staticmethod
    def load(filename, surface):
        try:
            with open(filename, 'rb') as file:
                obj = pickle.load(file)
                puzzle_found = RegularPuzzle.deserialize(obj, surface)
                if isinstance(puzzle_found, Puzzle):
                    return puzzle_found
                else:
                    return None
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, KeyError, FileNotFoundError):
            return None

    @staticmethod
    def deserialize(data, surface):
        puzzle = RegularPuzzle(surface, data['size_x'], data['size_y'], data['amount'], data['image_path'], data['rotatable'])
        puzzle.rowcols = data['rowcols']
        puzzle.pieces = {key: RegularPiece.deserialize(piece_data) for key, piece_data in data['pieces'].items()}
        puzzle.connected_groups = [{puzzle.pieces[pos] for pos in group} for group in data['connected_groups']]
        puzzle.active = puzzle.pieces[data['active']] if data['active'] else None
        puzzle.stopwatch.elapsed_time = int(data['stopwatch_time'])
        puzzle.save_path = data['save_path']
        return puzzle
