import pygame

from src.button import button
from src.game_state import game_state as state
from src.puzzle import puzzle

pygame.init()

#screen initialisation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Main menu")

#fonts
font = pygame.font.SysFont("arialblack",40)

#text colours
TEXT_COL = (255,255,255)

#game variables
game_state = state.MENU
puzzle = puzzle(50, 50, 600, 700, 33)
active_piece = None

def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def resize():
    start_button.change_position(screen.get_width()/2 - 50, screen.get_height()/2 - 5)
    resume_button.change_position(screen.get_width()/2 - 90, screen.get_height()/2 - 5)
    exit_button.change_position(screen.get_width()/2 - 60, screen.get_height() - 100)
    quit_button.change_position(screen.get_width()/2 - 50, screen.get_height()/2 + 55)

start_button = button(350, 295, 100,50,"Play", font, TEXT_COL, (42,68,81))
resume_button = button(310, 500, 180,50,"Resume", font, TEXT_COL, (42,68,81))
exit_button = button(340, 500, 100,50,"Exit", font, TEXT_COL, (42,68,81))
quit_button = button(350, 355, 100,50,"Quit", font, TEXT_COL, (42,68,81))

run = True
while run:

    screen.fill((52,78,91))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = state.PAUSED
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            if active_piece is not None:
                active_piece.move_piece(event.rel)

    match game_state:
        case state.PAUSED:
            display_text("Paused", font, TEXT_COL, screen.get_width() / 2 - 80, screen.get_height() / 6)
            if resume_button.draw(screen):
                game_state = state.PLAY
            if exit_button.draw(screen):
                game_state = state.MENU
        case state.MENU:
            display_text("Puzzle", font, TEXT_COL, screen.get_width() / 2 - 75, screen.get_height() / 6)
            if start_button.draw(screen):
                game_state = state.PLAY
            if quit_button.draw(screen):
                run = False
        case state.PLAY:
            active_piece = puzzle.draw(screen)
            pass
    resize()
    pygame.display.update()

pygame.quit()