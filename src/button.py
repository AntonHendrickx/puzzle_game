import pygame


class button:
    def __init__(self, x, y, sizeX, sizeY, text, font, txt_colour, btn_colour):
        self.rect = pygame.Rect(x, y, sizeX, sizeY)
        self.text = text
        self.font = font
        self.text_color = txt_colour
        self.button_color = btn_colour
        self.clicked = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        return action

    def change_position(self, newX, newY):
        self.rect.topleft = (newX, newY)
