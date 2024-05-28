import math

from src.regular_puzzle_piece import regular_piece

class puzzle:

    #use image later instead of rect
    def __init__(self, x, y, size_x, size_y, amount):
        self.amount = amount
        short, long = self.get_puzzle_divisions()
        if (short or long) == 1:
            raise AttributeError("amount of pieces is prime")
        if size_x > size_y:
            piece_dims = size_x / long, size_y / short
            amounts = long, short
        else:
            piece_dims = size_x / short, size_y / long
            amounts = short, long
        if not (0.6 < (piece_dims[0] / piece_dims[1]) < 1.6):
            raise AttributeError(f"too rectangular pieces: {piece_dims}, {amounts}")
        self.pieces = []
        self.create_pieces(x,y,amounts, piece_dims)

    def draw(self, surface):
        active = None
        for piece in self.pieces:
             if piece.draw(surface):
                 active = piece
        return active

    def get_puzzle_divisions(self):
        sroot = int(math.sqrt(self.amount))
        while self.amount % sroot != 0:
            sroot -= 1
        return sroot, self.amount // sroot

    def create_pieces(self, start_x, start_y, amounts, piece_dim):
        piece_width, piece_height = piece_dim
        cols, rows = amounts

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * piece_width
                y = start_y + row * piece_height
                self.pieces.append(regular_piece(x, y, piece_width, piece_height))