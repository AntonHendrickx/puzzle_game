import math

from src.regular_puzzle_piece import regular_piece
from src.timer import Timer

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
        self.pieces = {}
        self.create_pieces(x,y,amounts, piece_dims)
        self.active = None
        self.drag_timer = Timer(200)
        self.click = False

    def draw(self, surface):
        for (_,_), piece in self.pieces.items():
            piece.draw(surface)

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
                self.pieces[(row, col)] = regular_piece(x, y, piece_width, piece_height)

    def find_position(self, piece):
        key_list = list(self.pieces.keys())
        val_list = list(self.pieces.values())
        return key_list[val_list.index(piece)]

    def check_collisions(self, piece):
        piece_row, piece_col = self.find_position(piece)
        neighbors = [self.pieces.get(piece_row-1, piece_col),self.pieces.get(piece_row+1, piece_col),
                     self.pieces.get(piece_row, piece_col-1), self.pieces.get(piece_row, piece_col+1)]
        for neighbor in neighbors:
            if neighbor:
                if piece.check_collision(neighbor):
                    print("connection found!")
                    pass #connect the pieces!

    def move(self, rel):
        if self.active:
            self.active.move(rel)

    def handle_click(self, pos):
        if not self.click: #either click to pickup or drop
            self.click = True
            if not self.active:
                for (_,_) , piece in self.pieces.items():
                    if piece.click(pos):
                        self.active = piece
                        self.drag_timer.start()
                        break
            else:
                self.check_collisions(self.active)
                self.active = None


    def handle_click_stop(self):
        if self.drag_timer.is_time_up(): #dragging is active
            self.check_collisions(self.active)
            self.active = None
        self.drag_timer.stop()
        self.click = False

    def is_complete(self):
        return len(self.pieces) == 1