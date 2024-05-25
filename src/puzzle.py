import pygame

class puzzle:

    #use image later instead of rect
    def __init__(self, x, y, sizeX, sizeY):
        self.rect = pygame.Rect(x,y,sizeX,sizeY)
        #turn rect into list of pieces
        self.pieces = []

    def draw(self, surface):
        active = None
        for piece in self.pieces:
             if piece.draw(surface):
                 active = piece
        return active