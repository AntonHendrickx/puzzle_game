import pygame
from src.button import button
from src.game_state import game_state as state
from src.puzzle import puzzle

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Main menu")
        self.font = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COL = (255, 255, 255)
        self.game_state = state.MENU
        self.puzzle = puzzle(50, 50, 600, 700, 12)
        self.start_button = button(350, 295, 100, 50, "Play", self.font, self.TEXT_COL, (42, 68, 81))
        self.resume_button = button(310, 500, 180, 50, "Resume", self.font, self.TEXT_COL, (42, 68, 81))
        self.exit_button = button(340, 500, 100, 50, "Exit", self.font, self.TEXT_COL, (42, 68, 81))
        self.quit_button = button(350, 355, 100, 50, "Quit", self.font, self.TEXT_COL, (42, 68, 81))

    def display_text(self, text, x, y):
        img = self.font.render(text, True, self.TEXT_COL)
        self.screen.blit(img, (x, y))

    def resize(self):
        self.start_button.change_position(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2 - 5)
        self.resume_button.change_position(self.screen.get_width() / 2 - 90, self.screen.get_height() / 2 - 5)
        self.exit_button.change_position(self.screen.get_width() / 2 - 60, self.screen.get_height() - 100)
        self.quit_button.change_position(self.screen.get_width() / 2 - 50, self.screen.get_height() / 2 + 55)

    def run_game(self):
        run = True
        while run:
            self.screen.fill((52, 78, 91))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = state.PAUSED
                if event.type == pygame.QUIT:
                    run = False
                if self.game_state == state.PLAY:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.puzzle.handle_click_stop()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.puzzle.handle_click(pygame.mouse.get_pos())
                    elif event.type == pygame.MOUSEMOTION:
                        self.puzzle.move(event.rel)

            match self.game_state:
                case state.PAUSED:
                    self.display_text("Paused", self.screen.get_width() / 2 - 80, self.screen.get_height() / 6)
                    if self.resume_button.draw(self.screen):
                        self.game_state = state.PLAY
                    if self.exit_button.draw(self.screen):
                        self.game_state = state.MENU
                case state.MENU:
                    self.display_text("Puzzle", self.screen.get_width() / 2 - 75, self.screen.get_height() / 6)
                    if self.start_button.draw(self.screen):
                        self.game_state = state.PLAY
                    if self.quit_button.draw(self.screen):
                        run = False
                case state.PLAY:
                    self.puzzle.draw(self.screen)
            self.resize()
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()