import os
from abc import ABC, abstractmethod

import pygame

from src.button import button
from src.dropdown_menu import DropDownMenu
from src.puzzle import Puzzle


class State(ABC):

    def __init__(self, surface):
        self.font = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COL = (255, 255, 255)
        self.BACKGROUND = (42, 68, 81)
        self.surface = surface
        self.quit = False

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def resize(self):
        pass

    def display_text(self, text, x, y):
        text = self.font.render(text, True, self.TEXT_COL)
        self.surface.blit(text, (x, y))


class Menu(State):
    def __init__(self, surface):
        super().__init__(surface)
        self.start_button = button(350, 295, 100, 50, "Play", self.font, self.TEXT_COL, self.BACKGROUND)
        self.quit_button = button(350, 355, 100, 50, "Quit", self.font, self.TEXT_COL, self.BACKGROUND)

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.quit = True
        return new_state

    def draw(self):
        new_state = None
        x_pos = self.surface.get_width() / 2 - 75
        y_pos = self.surface.get_height() / 6
        self.display_text("Puzzle", x_pos, y_pos)
        if self.start_button.draw(self.surface):
            new_state = Selection(self.surface)
        if self.quit_button.draw(self.surface):
            self.quit = True

        return new_state

    def resize(self):
        self.start_button.change_position(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 5)
        self.quit_button.change_position(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 55)


class Selection(State):
    def __init__(self, surface):
        super().__init__(surface)
        self.image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        self.image_list = self.get_images()
        self.image_index = 0
        self.image = None
        self.load_image(self.image_list[0])
        self.rotate_setting = False
        self.piece_selector = DropDownMenu(self.surface, ["8", "18", "36"],
                                           (self.surface.get_width() / 2 + 70, self.surface.get_height() * 5 / 6))
        self.play_button = button(self.surface.get_width() / 2 - 60, self.surface.get_height() * 5 / 6, 120, 50,
                                  "Start", self.font, self.TEXT_COL, self.BACKGROUND)

    def is_image_file(self, filename):
        return filename.lower().endswith(self.image_extensions)

    def get_images(self):
        pathes = []
        for image in os.listdir("images/"):
            if self.is_image_file(image):
                pathes.append("images/" + image)
        return pathes

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        image_width, image_height = image.get_size()
        boundary_width = self.surface.get_width() * 2 / 3
        boundary_height = self.surface.get_height() * 2 / 3
        scale_factor = min(boundary_width / image_width, boundary_height / image_height)
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        self.image = pygame.transform.scale(image, (new_width, new_height))

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.image_index = max(self.image_index - 1, 0)
                        self.load_image(self.image_list[self.image_index])
                    elif event.key == pygame.K_RIGHT:
                        self.image_index = min(self.image_index + 1, len(self.image_list))
                        if self.image_index < len(self.image_list):
                            self.load_image(self.image_list[self.image_index])
                        else:
                            self.image = None
                case pygame.DROPFILE:
                    if self.image_index == len(self.image_list) and self.is_image_file(event.file):
                        self.image_list.append(event.file)
                        self.load_image(event.file)
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.piece_selector.clicked(pygame.mouse.get_pos())
                case pygame.QUIT:
                    self.quit = True
        return None

    def draw(self):
        new_state = None
        if self.image:
            rect = self.image.get_rect()
            screen_center_x, screen_center_y = self.surface.get_rect().center
            rect.center = (screen_center_x, screen_center_y - 50)
            self.surface.blit(self.image, rect)
        else:
            drag_rect = pygame.Rect(0, 0, self.surface.get_height() * 2 / 3, self.surface.get_height() * 2 / 3)
            screen_center_x, screen_center_y = self.surface.get_rect().center
            drag_rect.center = (screen_center_x, screen_center_y - 50)
            pygame.draw.rect(self.surface, self.BACKGROUND, drag_rect)
            self.display_text("Drag a file here to play!", screen_center_x-250, screen_center_y-70)
        if self.image_index > 0:
            rect_bottomleft = (self.surface.get_width() / 6, self.surface.get_height() * 5 / 6)
            points = [(rect_bottomleft[0], rect_bottomleft[1] + 10),
                      (rect_bottomleft[0] - 25, rect_bottomleft[1] + 30),
                      (rect_bottomleft[0], rect_bottomleft[1] + 50)]
            pygame.draw.polygon(self.surface, self.TEXT_COL, points)  # arrow to right
        if self.image_index < len(self.image_list):
            rect_bottomright = (self.surface.get_width() * 5 / 6, self.surface.get_height() * 5 / 6)
            points = [(rect_bottomright[0], rect_bottomright[1] + 10),
                      (rect_bottomright[0] + 25, rect_bottomright[1] + 30),
                      (rect_bottomright[0], rect_bottomright[1] + 50)]
            pygame.draw.polygon(self.surface, self.TEXT_COL, points)  # arrow to left
        if self.play_button.draw(self.surface):
            if self.image_index != len(self.image_list):
                puzzle = Puzzle.load("saves/" + self.image_list[self.image_index].replace("images/", "") +
                                     self.piece_selector.selected_option + ".pkl", self.surface)
                if not puzzle:
                    try:
                        new_state = Play.from_new_puzzle(self.surface, self.image.get_rect().width,
                                                         self.image.get_rect().height,
                                                         int(self.piece_selector.selected_option),
                                                         self.image_list[self.image_index], self.rotate_setting)
                    except AttributeError:
                        # show an error
                        new_state = None
                else:
                    new_state = Play.from_existing_puzzle(self.surface, puzzle)
        self.piece_selector.draw_dropdown()
        return new_state

    def resize(self):
        self.play_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() * 5 / 6)
        self.piece_selector.set_position((self.surface.get_width() / 2 + 70, self.surface.get_height() * 5 / 6))


class Play(State):
    def __init__(self, surface, puzzle):
        super().__init__(surface)
        self.puzzle = puzzle
        self.savefile_path = "saves/" + puzzle.image_path.replace("images/", "") + str(self.puzzle.amount) + ".pkl"

    @classmethod
    def from_new_puzzle(cls, surface, size_x, size_y, amount, image_path, rotatable=False):
        puzzle = Puzzle(surface, size_x, size_y, amount, image_path, rotatable)
        return cls(surface, puzzle)

    @classmethod
    def from_existing_puzzle(cls, surface, puzzle):
        return cls(surface, puzzle)

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.MOUSEBUTTONUP:
                    self.puzzle.handle_click_stop()
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.puzzle.handle_click(pygame.mouse.get_pos())
                case pygame.MOUSEMOTION:
                    self.puzzle.move(event.rel)
                case pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.puzzle.rotate(False)
                    elif event.key == pygame.K_t:
                        self.puzzle.rotate(True)
                    elif event.key == pygame.K_ESCAPE:
                        self.puzzle.pause_stopwatch()
                        new_state = Paused(self.surface, self.puzzle)
                case pygame.QUIT:
                    self.puzzle.save_to_file(self.savefile_path)
                    self.quit = True
        return new_state

    def draw(self):
        self.puzzle.draw(self.surface)
        if self.puzzle.is_complete():
            self.puzzle.clearsave(self.savefile_path)
            return Menu(self.surface)

    def resize(self):
        return


class Paused(State):
    def __init__(self, surface, puzzle):
        super().__init__(surface)
        self.resume_button = button(310, 500, 180, 50, "Resume", self.font, self.TEXT_COL,
                                    self.BACKGROUND)
        self.options_button = button(310, 400, 180, 50, "Options", self.font, self.TEXT_COL,
                                     self.BACKGROUND)
        self.exit_button = button(340, 500, 100, 50, "Exit", self.font, self.TEXT_COL,
                                  self.BACKGROUND)
        self.puzzle = puzzle

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        new_state = Play(self.surface, self.puzzle)
                        self.puzzle.pause_stopwatch()
                case pygame.QUIT:
                    self.puzzle.save_to_file()
                    self.quit = True
        return new_state

    def draw(self):
        new_state = None
        self.display_text("Paused", self.surface.get_width() / 2 - 80, self.surface.get_height() / 6)
        if self.resume_button.draw(self.surface):
            new_state = Play.from_existing_puzzle(self.surface, self.puzzle)
            self.puzzle.pause_stopwatch()
        if self.exit_button.draw(self.surface):
            self.puzzle.save_to_file()
            new_state = Menu(self.surface)
        if self.options_button.draw(self.surface):
            new_state = Options(self.surface, self.puzzle)
        return new_state

    def resize(self):
        self.resume_button.change_position(self.surface.get_width() / 2 - 90, self.surface.get_height() / 2 - 5)
        self.exit_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() - 100)
        self.options_button.change_position(self.surface.get_width() / 2 - 90, self.surface.get_height() * 2 / 3)


class Options(State):
    def __init__(self, surface, puzzle):
        super().__init__(surface)
        self.smallfont = pygame.font.SysFont("arialblack",20)
        self.puzzle = puzzle
        self.back_button = button(340, 465, 120, 50, "Back", self.font, self.TEXT_COL,
                                  self.BACKGROUND)
        self.stopwatch_toggle = button(430,300, 30, 30, "", self.smallfont,
                                       self.TEXT_COL, self.BACKGROUND)

    def display_small_text(self, text, x, y):
        text = self.smallfont.render(text, True, self.TEXT_COL)
        self.surface.blit(text, (x, y))

    def handle_events(self, events):
        new_state = None
        for event in events:
            if event.type == pygame.QUIT:
                self.puzzle.save_to_file()
                self.quit = True
        return new_state

    def draw(self):
        new_state = None
        self.display_text("Options", self.surface.get_width() / 2 - 90, self.surface.get_height() / 6)
        self.display_small_text("Hide timer", self.surface.get_width() * 2 / 5 , self.surface.get_height() / 2 + 10)
        if self.back_button.draw(self.surface):
            new_state = Paused(self.surface, self.puzzle)
        if self.stopwatch_toggle.draw(self.surface):
            self.puzzle.stopwatch.hide_show()
        if self.puzzle.stopwatch.visible:
            self.stopwatch_toggle.button_color = self.BACKGROUND
        else:
            self.stopwatch_toggle.button_color = (240, 240, 240)
        return new_state

    def resize(self):
        self.back_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() * 3 / 4 + 15)
        self.stopwatch_toggle.change_position(self.surface.get_width() / 2 + 30, self.surface.get_height() / 2 + 10)
