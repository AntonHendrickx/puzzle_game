import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main menu")

font = pygame.font.SysFont("arialblack",40)

TEXT_COL = (255,255,255)

def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
while run:

    screen.fill((52,78,91))

    display_text("Main menu",font, TEXT_COL, 300, 250)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()