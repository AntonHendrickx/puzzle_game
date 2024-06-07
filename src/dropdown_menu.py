import pygame


class DropDownMenu:

    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 50
    FONT_SIZE = 30
    FONT_SMALL_SIZE = 20
    DROPDOWN_POS_X = 50
    DROPDOWN_POS_Y = 50
    OPTION_HEIGHT = 40

    def __init__(self, surface, options, position=(DROPDOWN_POS_X, DROPDOWN_POS_Y), dims=(BUTTON_WIDTH,BUTTON_HEIGHT, FONT_SIZE, FONT_SMALL_SIZE, OPTION_HEIGHT)):
        self.surface = surface
        self.show_options = False
        self.options = options
        self.selected_option = options[0]
        self.position = position
        self.dims = dims
        self.colors = {
            "background": (240, 240, 240),
            "text": (50, 50, 50),
            "button_bg": (200, 200, 200),
            "button_border": (150, 150, 150),
            "button_hover": (220, 220, 220),
            "dropdown_bg": (220, 220, 220),
            "dropdown_border": (150, 150, 150),
            "dropdown_hover": (200, 200, 200),
            "dropdown_text": (50, 50, 50),
        }

    def draw_dropdown(self):
        # Draw dropdown button
        button_color = self.colors["button_hover"] if self.show_options else self.colors["button_bg"]
        pygame.draw.rect(self.surface, button_color, (self.position[0], self.position[1], self.dims[0], self.dims[1]))
        pygame.draw.rect(self.surface, self.colors["button_border"], (self.position[0], self.position[1], self.dims[0], self.dims[1]),
                         2)

        # Render and position the text on the button
        font = pygame.font.Font(None, self.dims[2])
        text_surface = font.render(self.selected_option, True, self.colors["text"])
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.dims[0] / 2, self.position[1] + self.dims[1] / 2))
        self.surface.blit(text_surface, text_rect)

        # Draw dropdown options if the dropdown is expanded
        if self.show_options:
            # Draw each dropdown option
            for i, option in enumerate(self.options):
                option_y = self.position[1] + self.dims[1] + i * self.dims[4]
                option_rect = pygame.Rect(self.position[0], option_y, self.dims[0], self.dims[4])
                option_color = self.colors["dropdown_hover"] if option_rect.collidepoint(pygame.mouse.get_pos()) else self.colors[
                    "dropdown_bg"]
                pygame.draw.rect(self.surface, option_color, option_rect)
                pygame.draw.rect(self.surface, self.colors["dropdown_border"], option_rect, 2)

                # Render and position the text for each option
                option_font = pygame.font.Font(None, self.dims[3])
                option_surface = option_font.render(option, True, self.colors["dropdown_text"])
                option_rect = option_surface.get_rect(
                    center=(self.position[0] + self.dims[0] / 2, option_y + self.dims[4] / 2))
                self.surface.blit(option_surface, option_rect)

    def clicked(self, pos):
        if self.show_options:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.position[0], self.position[1] + self.dims[1] + i * self.dims[4],
                                          self.dims[0], self.dims[4])
                if option_rect.collidepoint(pos):
                    self.selected_option = option
                    self.show_options = False
                    break
        else:
            # Toggle dropdown visibility if the button is clicked
            if pygame.Rect(self.position[0], self.position[1], self.dims[0], self.dims[1]).collidepoint(pos):
                self.show_options = not self.show_options
