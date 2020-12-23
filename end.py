import pygame
pygame.init()


WIDTH = 400
HEADER = 30
HEIGHT = WIDTH + HEADER
WINDOW = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(WINDOW)

COLOR_CYAN = (0, 255, 255)
COLOR_BLACK = (0, 0, 0)

FONT_SIZE = 16
FONT = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE)

BUTTONS = []
def draw_button(x, y, len, height, text):
    pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(text, True, COLOR_BLACK)
    text_len = text.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


def draw_text(x, y, len, text):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(text, True, COLOR_BLACK)
    text_len = text.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


SCREEN.fill(COLOR_CYAN)
draw_text(2, 2, WIDTH - 4, 'Game Over!!!')
draw_button(2, 60, WIDTH - 4, HEADER - 4, 'Play Again')
draw_button(2, 100, WIDTH - 4, HEADER - 4, 'Exit')

