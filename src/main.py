import pygame

from src.button import button

pygame.init()

#screen initialisation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main menu")

#fonts
font = pygame.font.SysFont("arialblack",40)

#text colours
TEXT_COL = (255,255,255)

#game variables
game_paused = False

def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

quit_button = button(300, 350, 100,50,"Quit", font, TEXT_COL, (42,68,81))

run = True
while run:

    screen.fill((52,78,91))

    display_text("Main menu",font, TEXT_COL, 300, 250)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
        if event.type == pygame.QUIT:
            run = False

    if game_paused:
        display_text("Paused", font, TEXT_COL, 300, 300)

    if quit_button.draw(screen):
        run = False

    pygame.display.update()

pygame.quit()