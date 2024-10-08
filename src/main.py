import pygame
from game_state import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Puzzle Game")
        self.game_state = Menu(self.screen)
        self.game_clock = pygame.time.Clock()

    def run_game(self):
        run = True
        while run:
            self.game_clock.tick(100)
            events = pygame.event.get()
            next_state_1 = self.game_state.handle_events(events)
            next_state_2 = self.game_state.draw()
            self.game_state.resize()

            if self.game_state.quit:
                run = False
            if next_state_1 is not None:
                self.game_state = next_state_1
            elif next_state_2 is not None:
                self.game_state = next_state_2
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()
