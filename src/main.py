import pygame

from src.button import button

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
game_paused = False
play = False

def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def resize():
    start_button.change_position(screen.get_width()/2 - 50, screen.get_height()/2 - 5)
    back_button.change_position(screen.get_width()/2 - 60, screen.get_height() - 100)
    quit_button.change_position(screen.get_width()/2 - 50, screen.get_height()/2 + 55)

start_button = button(350, 295, 100,50,"Play", font, TEXT_COL, (42,68,81))
back_button = button(340, 500, 120,50,"Back", font, TEXT_COL, (42,68,81))
quit_button = button(350, 355, 100,50,"Quit", font, TEXT_COL, (42,68,81))

run = True
while run:

    screen.fill((52,78,91))

    display_text("Puzzle",font, TEXT_COL, screen.get_width()/2-75, screen.get_height()/6)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
        if event.type == pygame.QUIT:
            run = False

    if game_paused:
        display_text("Paused", font, TEXT_COL, screen.get_width()/2 - 80, screen.get_height()/2)
    if play:
        if back_button.draw(screen):
            play = False
    else:
        if start_button.draw(screen):
            play = True

        if quit_button.draw(screen):
            run = False
    resize()
    pygame.display.update()

pygame.quit()