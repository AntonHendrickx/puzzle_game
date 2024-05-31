import math
import random
import pygame.image

from src.regular_puzzle_piece import regular_piece
from src.timer import Timer

class puzzle:

    #use image later instead of rect
    def __init__(self, surface, size_x, size_y, amount, image_path):
        self.amount = amount
        self.pieces = {}
        self.amounts = ()
        piece_dims = self.__set_piece_dims(size_x, size_y, amount)
        self.create_pieces(surface, self.amounts, piece_dims)
        self.active = None
        self.drag_timer = Timer(200)
        self.click = False
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (size_x, size_y))

    def draw(self, surface):
        for (row,col), piece in self.pieces.items():
            piece_image = self.get_piece_image(row, col, piece.get_width(), piece.get_height())
            piece.draw(surface, piece_image)

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
                square_height = height / factor_h

                if within_ratio(square_width, square_height):
                    self.amounts = (factor_w, factor_h)
                    return square_width, square_height

        raise AttributeError("Invalid square amount")

    def create_pieces(self,surface, amounts, piece_dim):
        piece_width, piece_height = piece_dim
        cols, rows = amounts
        screen_width, screen_height = surface.get_size()

        for row in range(rows):
            for col in range(cols):
                x = random.randint(0, int(screen_width - piece_width))
                y = random.randint(0, int(screen_height - piece_height))
                self.pieces[(row, col)] = regular_piece(x, y, piece_width, piece_height)

    def find_position(self, piece):
        key_list = list(self.pieces.keys())
        val_list = list(self.pieces.values())
        return key_list[val_list.index(piece)]

    def get_piece_image(self, row, col, width, height):
        x = col * width
        y = row * height
        return self.image.subsurface(pygame.Rect(x, y, width, height))

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
                #self.check_collisions(self.active)
                self.active = None


    def handle_click_stop(self):
        if self.drag_timer.is_time_up(): #dragging is active
            #self.check_collisions(self.active)
            self.active = None
        self.drag_timer.stop()
        self.click = False

    def is_complete(self):
        return len(self.pieces) == 1