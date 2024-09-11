import pygame
import audio_handler


class Button:
    def __init__(self, x, y, size_x, size_y, text, font, txt_colour, btn_colour, sound=1):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.text = text
        self.font = font
        self.text_colour = txt_colour
        self.button_colour = btn_colour
        self.clicked = False
        self.sound = "resources/button{}.wav".format(sound)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                audio_handler.play_sound(self.sound)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, self.button_colour, self.rect)
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        return action

    def change_position(self, new_x, new_y):
        self.rect.topleft = (new_x, new_y)

    def style(self, text_col, button_col):
        self.button_colour = button_col
        self.text_colour = text_col
