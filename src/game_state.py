import os
import pygame

from abc import ABC, abstractmethod
from button import Button
from dropdown_menu import DropDownMenu
from puzzle import Puzzle
from regular_puzzle import RegularPuzzle
from src.square_puzzle import SquarePuzzle


class State(ABC):

    COLS = {
        'white': (255, 255, 255),
        'red': (139, 0, 0),
        'orange': (255, 140, 0),
        'yellow': (255, 215, 0),
        'lime': (50, 205, 50),
        'green': (34, 139, 34),
        'lightblue': (130, 150, 189),
        'cyan': (52, 78, 91),
        'darkblue': (42, 68, 81),
        'gray': (169, 169, 169)
    }

    def __init__(self, surface, background_col = COLS.get('cyan')):
        self.font = pygame.font.SysFont("arialblack", 40)
        self.smallfont = pygame.font.SysFont("arialblack", 20)
        self.TEXT_COL = self.COLS.get('white')
        self.BACKGROUND = background_col
        self.BUTTON_COL = self.COLS.get('darkblue')
        self.surface = surface
        self.quit = False

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def draw(self):
        self.surface.fill(self.BACKGROUND)
        return

    @abstractmethod
    def resize(self):
        pass

    def display_text(self, text, x, y):
        text = self.font.render(text, True, self.TEXT_COL)
        self.surface.blit(text, (x, y))

    def display_small_text(self, text, x, y):
        text = self.smallfont.render(text, True, self.TEXT_COL)
        self.surface.blit(text, (x, y))


class Menu(State):
    def __init__(self, surface):
        super().__init__(surface)
        self.start_button = Button(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 5, 100, 50,
                                   "Play", self.font, self.TEXT_COL, self.BUTTON_COL)
        self.quit_button = Button(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 55, 100, 50,
                                  "Quit", self.font, self.TEXT_COL, self.BUTTON_COL)

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.quit = True
        return new_state

    def draw(self):
        new_state = None
        super().draw()
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
        if self.image is not None:
            self.piece_selector = DropDownMenu(self.surface,
                                               [str(x) for x in Puzzle.get_possible_piece_dims(
                                                   self.image.get_rect().width, self.image.get_rect().width)],
                                               (self.surface.get_width() / 12 - 35, self.surface.get_height() / 2))
        self.play_button = Button(self.surface.get_width() / 2 - 60, self.surface.get_height() * 5 / 6, 120, 50,
                                  "Start", self.font, self.TEXT_COL, self.BUTTON_COL)
        self.rotation_toggle = Button(self.surface.get_width() / 4 + 50, self.surface.get_height() * 5 / 6 + 15,
                                      30, 30, "", self.smallfont, self.TEXT_COL, self.BUTTON_COL)
        self.type_selector = DropDownMenu(self.surface, ["regular", "square"],
                                          (self.surface.get_width() * 3 / 4, self.surface.get_height() * 5 / 6))

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
                            if self.image is not None:
                                self.piece_selector.options = [str(x) for x in Puzzle.get_possible_piece_dims(
                                    self.image.get_rect().width, self.image.get_rect().width)]
                        else:
                            self.image = None
                case pygame.DROPFILE:
                    if self.image_index == len(self.image_list) and self.is_image_file(event.file):
                        self.image_list.append(event.file)
                        self.load_image(event.file)
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.piece_selector.clicked(pygame.mouse.get_pos())
                        self.type_selector.clicked(pygame.mouse.get_pos())
                    elif event.button == 4:
                        self.piece_selector.scroll('up')
                        self.type_selector.scroll('up')
                    elif event.button == 5:
                        self.piece_selector.scroll('down')
                        self.type_selector.scroll('down')
                case pygame.QUIT:
                    self.quit = True
        return None

    def draw_puzzle_image(self):
        if self.image:
            rect = self.image.get_rect()
            screen_center_x, screen_center_y = self.surface.get_rect().center
            rect.center = (screen_center_x - 100, screen_center_y)
            self.surface.blit(self.image, rect)
        else:
            drag_rect = pygame.Rect(0, 0, self.surface.get_height() * 2 / 3, self.surface.get_height() * 2 / 3)
            screen_center_x, screen_center_y = self.surface.get_rect().center
            drag_rect.center = (screen_center_x - 100, screen_center_y)
            pygame.draw.rect(self.surface, self.BUTTON_COL, drag_rect)
            self.display_text("Drag a file here to play!", screen_center_x * 2 / 5, screen_center_y - 30)

    def draw_arrows(self):
        if self.image_index > 0:
            top_point = (self.surface.get_width() * 2 / 5, self.surface.get_height() * 1 / 6 - 20)
            points = [(top_point[0], top_point[1]),
                      (top_point[0] + 20, top_point[1] - 20),
                      (top_point[0] + 40, top_point[1])]
            pygame.draw.polygon(self.surface, self.TEXT_COL, points)  # arrow down
        if self.image_index < len(self.image_list):
            top_point = (self.surface.get_width() * 2 / 5, self.surface.get_height() * 5 / 6 + 20)
            points = [(top_point[0], top_point[1]),
                      (top_point[0] + 20, top_point[1] + 20),
                      (top_point[0] + 40, top_point[1])]
            pygame.draw.polygon(self.surface, self.TEXT_COL, points)  # arrow up

    def draw(self):
        new_state = None
        super().draw()
        self.draw_puzzle_image()
        self.draw_arrows()
        if self.play_button.draw(self.surface):
            if self.image_index != len(self.image_list):
                puzzle = None
                if self.type_selector.selected_option == 'regular':
                    puzzle = RegularPuzzle.load("saves/" + self.type_selector.selected_option +
                                                self.image_list[self.image_index].replace("images/", "") +
                                                self.piece_selector.selected_option + ".pkl", self.surface)
                elif self.type_selector.selected_option == 'square':
                    puzzle = SquarePuzzle.load("saves/" + self.type_selector.selected_option +
                                               self.image_list[self.image_index].replace("images/", "") +
                                               self.piece_selector.selected_option + ".pkl", self.surface)
                if not puzzle:
                    try:
                        new_state = Play.from_new_puzzle(self.type_selector.selected_option, self.surface, self.BACKGROUND,
                                                         self.image.get_rect().width, self.image.get_rect().height,
                                                         int(self.piece_selector.selected_option), self.image_list[
                                                             self.image_index], self.rotate_setting)
                    except AttributeError:
                        # show an error
                        new_state = None
                else:
                    new_state = Play.from_existing_puzzle(self.surface, self.BACKGROUND, puzzle, self.type_selector.selected_option)
        self.piece_selector.draw_dropdown()
        self.type_selector.draw_dropdown()
        self.display_small_text("Rotation", self.surface.get_width() * 5 / 6 - 30, self.surface.get_height() *
                                5 / 6 - 60)
        if self.rotation_toggle.draw(self.surface):
            self.rotate_setting = not self.rotate_setting
        if self.rotate_setting:
            self.rotation_toggle.button_color = (240, 240, 240)
        else:
            self.rotation_toggle.button_color = self.BUTTON_COL
        return new_state

    def resize(self):
        self.play_button.change_position(self.surface.get_width() * 4 / 5 + 10, self.surface.get_height() * 5 / 6)
        self.piece_selector.set_position((self.surface.get_width() * 4 / 5 + 30, self.surface.get_height() / 3))
        self.rotation_toggle.change_position(self.surface.get_width() * 5 / 6 + 70, self.surface.get_height() *
                                             5 / 6 - 60)
        self.type_selector.set_position((self.surface.get_width() * 4 / 5 + 30, self.surface.get_height() * 3 / 5))


class Play(State):
    def __init__(self, surface, background_col, puzzle, puzz_type='', from_save = False):
        super().__init__(surface, background_col)
        self.puzzle = puzzle
        if puzz_type != '' and not from_save:
            self.savefile_path = ("saves/" + puzz_type + puzzle.image_path.replace("images/", "") +
                                                    str(self.puzzle.get_amount()) + ".pkl")
            self.puzzle.save_path = self.savefile_path
            self.puzz_type = puzz_type
        elif from_save:
            self.savefile_path = self.puzzle.save_path

    @classmethod
    def from_new_puzzle(cls, puzz_type, surface, background_col, size_x, size_y, amount, image_path, rotatable=False):
        puzzle = None
        if puzz_type == 'regular':
            puzzle = RegularPuzzle(surface, size_x, size_y, amount, image_path, rotatable)
        elif puzz_type == 'square':
            puzzle = SquarePuzzle(surface, size_x, size_y, amount, image_path, rotatable)
        return cls(surface, background_col, puzzle, puzz_type, False)

    @classmethod
    def from_existing_puzzle(cls, surface, background_col, puzzle, puzz_type=''):
        return cls(surface, background_col, puzzle, puzz_type, True)

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
                        new_state = Paused(self.surface, self.puzzle, self.BACKGROUND)
                case pygame.QUIT:
                    self.puzzle.save_to_file(self.savefile_path)
                    self.quit = True
        return new_state

    def draw(self):
        super().draw()
        self.puzzle.draw(self.surface)
        if self.puzzle.is_complete():
            self.puzzle.clearsave(self.savefile_path)
            return Menu(self.surface)

    def resize(self):
        return


class Paused(State):
    def __init__(self, surface, puzzle, background_col):
        super().__init__(surface, background_col)
        self.resume_button = Button(310, 500, 180, 50, "Resume", self.font, self.TEXT_COL,
                                    self.BUTTON_COL)
        self.options_button = Button(310, 400, 180, 50, "Options", self.font, self.TEXT_COL,
                                     self.BUTTON_COL)
        self.exit_button = Button(340, 500, 100, 50, "Exit", self.font, self.TEXT_COL,
                                  self.BUTTON_COL)
        self.puzzle = puzzle

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        new_state = Play(self.surface, self.BACKGROUND, self.puzzle)
                        self.puzzle.pause_stopwatch()
                case pygame.QUIT:
                    self.puzzle.save_to_file()
                    self.quit = True
        return new_state

    def draw(self):
        new_state = None
        super().draw()
        self.display_text("Paused", self.surface.get_width() / 2 - 80, self.surface.get_height() / 6)
        if self.resume_button.draw(self.surface):
            new_state = Play.from_existing_puzzle(self.surface, self.BACKGROUND, self.puzzle)
            self.puzzle.pause_stopwatch()
        if self.exit_button.draw(self.surface):
            self.puzzle.save_to_file()
            new_state = Menu(self.surface)
        if self.options_button.draw(self.surface):
            new_state = Options(self.surface, self.puzzle, self.BACKGROUND)
        return new_state

    def resize(self):
        self.resume_button.change_position(self.surface.get_width() / 2 - 90, self.surface.get_height() / 2 - 5)
        self.exit_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() - 100)
        self.options_button.change_position(self.surface.get_width() / 2 - 90, self.surface.get_height() * 2 / 3)


class Options(State):
    def __init__(self, surface, puzzle, background_col):
        super().__init__(surface, background_col)
        self.puzzle = puzzle
        self.back_button = Button(340, 465, 120, 50, "Back", self.font, self.TEXT_COL,
                                  self.BUTTON_COL)
        self.stopwatch_toggle = Button(430, 300, 30, 30, "", self.smallfont,
                                       self.TEXT_COL, self.BUTTON_COL)
        self.colour_select = DropDownMenu(self.surface, list(self.COLS.keys()), (self.surface.get_width() * 3 / 4,
                                                                        self.surface.get_height() / 2 + 10))
        self.colour_select.selected_option = list(self.COLS.keys())[list(self.COLS.values()).index(self.BACKGROUND)]

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.puzzle.save_to_file()
                    self.quit = True
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.colour_select.clicked(pygame.mouse.get_pos())
                        self.BACKGROUND = self.COLS.get(self.colour_select.selected_option)
                    elif event.button == 4:
                        self.colour_select.scroll('up')
                    elif event.button == 5:
                        self.colour_select.scroll('down')
        return new_state

    def draw(self):
        new_state = None
        super().draw()
        self.display_text("Options", self.surface.get_width() / 2 - 90, self.surface.get_height() / 6)
        self.display_small_text("Hide timer", self.surface.get_width() * 2 / 5, self.surface.get_height() / 2 + 10)
        if self.back_button.draw(self.surface):
            new_state = Paused(self.surface, self.puzzle, self.BACKGROUND)
        if self.stopwatch_toggle.draw(self.surface):
            self.puzzle.stopwatch.hide_show()
        if self.puzzle.stopwatch.visible:
            self.stopwatch_toggle.button_color = self.BUTTON_COL
        else:
            self.stopwatch_toggle.button_color = (240, 240, 240)
        self.colour_select.draw_dropdown()
        return new_state

    def resize(self):
        self.back_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() * 3 / 4 + 15)
        self.stopwatch_toggle.change_position(self.surface.get_width() / 2 + 30, self.surface.get_height() / 2 + 10)
        self.colour_select.set_position((self.surface.get_width() * 3 / 4, self.surface.get_height() / 2 + 10))
