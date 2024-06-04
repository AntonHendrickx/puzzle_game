from abc import ABC, abstractmethod

import pygame

from src.button import button
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
        self.surface.blit(text, (x,y))

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
            puzzle = Puzzle.load("saves/savefile.pkl", self.surface)
            if not puzzle:
                new_state = Play.from_new_puzzle(self.surface, 600, 300, 8, "images/puzzle_test.png")
            else:
                new_state = Play.from_existing_puzzle(self.surface, puzzle)
            #start selection screen (for now play)
        if self.quit_button.draw(self.surface):
            self.quit = True

        return new_state

    def resize(self):
        self.start_button.change_position(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 - 5)
        self.quit_button.change_position(self.surface.get_width() / 2 - 50, self.surface.get_height() / 2 + 55)

class Selection(State):
    def __init__(self, surface):
        super().__init__(surface)

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.DROPFILE:
                    pass #check if valid image, then create puzzle or something
                case pygame.QUIT:
                    self.quit = True

    def draw(self):
        pass

    def resize(self):
        pass


class Play(State):
    def __init__(self, surface, puzzle):
        super().__init__(surface)
        self.puzzle = puzzle
        self.savefile_path = "saves/savefile.pkl"

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
        self.resume_button = button(310, 500, 180, 50, "Resume", self.font, self.TEXT_COL, self.BACKGROUND)
        self.options_button = button(310, 400, 180, 50, "Options", self.font, self.TEXT_COL, self.BACKGROUND)
        self.exit_button = button(340, 500, 100, 50, "Exit", self.font, self.TEXT_COL, self.BACKGROUND)
        self.puzzle = puzzle

    def handle_events(self, events):
        new_state = None
        for event in events:
            match event.type:
                case pygame.K_ESCAPE:
                    new_state = Play(self.surface, self.puzzle)
        return new_state

    def draw(self):
        new_state = None
        self.display_text("Paused", self.surface.get_width() / 2 - 80, self.surface.get_height() / 6)
        if self.resume_button.draw(self.surface):
            new_state = Play.from_existing_puzzle(self.surface, self.puzzle)
        if self.exit_button.draw(self.surface):
            self.puzzle.save_to_file("saves/savefile.pkl")
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
        self.puzzle = puzzle
        self.back_button = button(340, 465, 120, 50, "Back", self.font, self.TEXT_COL, self.BACKGROUND)

    def handle_events(self, events):
        new_state = None
        for event in events:
            if event.type == pygame.QUIT:
                self.puzzle.save_to_file("saves/savefile.pkl")
                new_state = True
        return new_state

    def draw(self):
        new_state = None
        self.display_text("Options", self.surface.get_width() / 2 - 90, self.surface.get_height() / 6)
        if self.back_button.draw(self.surface):
            new_state = Paused(self.surface, self.puzzle)

        return new_state

    def resize(self):
        self.back_button.change_position(self.surface.get_width() / 2 - 60, self.surface.get_height() * 3 / 4 + 15)