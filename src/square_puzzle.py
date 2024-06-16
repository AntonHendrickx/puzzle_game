import pickle
import random

from src.puzzle import Puzzle
from src.square_puzzle_piece import SquarePiece


class SquarePuzzle(Puzzle):
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
                self.pieces[(row, col)] = SquarePiece(x, y, piece_width, piece_height, piece_image, rotation)

    def serialize(self):
        return {
            'type': 'square',
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
                puzzle_found = SquarePuzzle.deserialize(obj, surface)
                if isinstance(puzzle_found, Puzzle):
                    return puzzle_found
                else:
                    return None
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError, KeyError, FileNotFoundError):
            return None

    @staticmethod
    def deserialize(data, surface):
        puzzle = SquarePuzzle(surface, data['size_x'], data['size_y'], data['amount'], data['image_path'], data['rotatable'])
        puzzle.rowcols = data['rowcols']
        puzzle.pieces = {key: SquarePiece.deserialize(piece_data) for key, piece_data in data['pieces'].items()}
        puzzle.connected_groups = [{puzzle.pieces[pos] for pos in group} for group in data['connected_groups']]
        puzzle.active = puzzle.pieces[data['active']] if data['active'] else None
        puzzle.stopwatch.elapsed_time = int(data['stopwatch_time'])
        puzzle.save_path = data['save_path']
        return puzzle
