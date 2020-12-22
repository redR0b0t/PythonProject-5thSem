# coding = utf-8
import threading

import pygame

from maze_generator import generate_maze
from maze_solver import solve_maze
from maze_solver import AI
from maze_solver import SCORE
from utils import stop_thread
import random

pygame.init()

WIDTH = 400
HEADER = 30
BOTTOM = 60
HEIGHT = WIDTH + HEADER + BOTTOM
WINDOW = (WIDTH, HEIGHT)

TITLE = "Python Project 5th sem"
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption(TITLE)
FPS = 60
CLOCK = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 160, 122)
COLOR_CYAN = (0, 255, 255)

FONT_SIZE = 16
FONT = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE)

BUTTONS = []

SOLVE_THREAD = None

r1 = r2 = 0


def draw_rect(x, y, len, color):
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)


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


def refresh():
    global MAZE, ENTRANCE, EXIT, SOLVE_THREAD
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    size = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    SOLVE_THREAD.start()


def draw_menu():
    SCREEN.fill(COLOR_CYAN)
    draw_text(2, 2, WIDTH - 4, 'Menu')
    draw_button(2, 60, WIDTH - 4, HEADER - 4, 'Easy')
    draw_button(2, 100, WIDTH - 4, HEADER - 4, 'Medium')
    draw_button(2, 140, WIDTH - 4, HEADER - 4, 'Hard')

    draw_text(200, 240, WIDTH - 4, 'Jatin Yadav')
    draw_text(200, 280, WIDTH - 4, 'Gopi kishan')
    draw_text(200, 320, WIDTH - 4, 'Kishore H')

    # if len(BUTTONS) == 0:
    BUTTONS.append({
        'x': 2,
        'y': 60,
        'length': WIDTH - 4,
        'height': HEADER - 4,
        'click': easy
    })

    BUTTONS.append({
        'x': 2,
        'y': 100,
        'length': WIDTH - 4,
        'height': HEADER - 4,
        'click': medium
    })

    BUTTONS.append({
        'x': 2,
        'y': 140,
        'length': WIDTH - 4,
        'height': HEADER - 4,
        'click': hard
    })

    pygame.display.flip()


def easy():
    global r1
    global r2
    r1 = 5
    r2 = 10
    refresh()


def medium():
    global r1
    global r2
    r1 = 10
    r2 = 15
    refresh()


def hard():
    global r1
    global r2
    r1 = 15
    r2 = 20
    refresh()


def draw_maze(maze, cur_pos, score):
    SCREEN.fill(COLOR_WHITE)
    draw_button(2, 2, WIDTH - 4, HEADER - 4, 'Toggle Level')
    BUTTONS.clear()
    BUTTONS.append({
        'x': 2,
        'y': 2,
        'length': WIDTH - 4,
        'height': HEADER - 4,
        'click': refresh
    })

    size = len(maze)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2
    # cell_padding = -100
    for y in range(size):
        for x in range(size):
            cell = maze[y][x]
            color = COLOR_BLACK if cell == 1 else COLOR_RED if cell == 3 else COLOR_CYAN if cell == 2 else COLOR_WHITE
            if x == cur_pos[1] and y == cur_pos[2]:
                color = COLOR_BLUE
            if color == COLOR_BLACK:
                draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size, color)
                # draw_rect(cell_padding + x * cell_size+1, HEADER + cell_padding + y * cell_size+1, cell_size - 1, color)
            else:
                draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)

    draw_button(2, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, 'Score')
    draw_text(1, HEIGHT - BOTTOM + 20, WIDTH // 3, str(score))
    draw_button(2 + WIDTH // 3, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, 'Menu')
    draw_button(2 + 2 * (WIDTH // 3), HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, 'AI')

    BUTTONS.append({
        'x': 2,
        'y': 60,
        'length': WIDTH - 4,
        'height': HEADER - 4,
        'click': easy
    })

    pygame.display.flip()


def dispatcher_click(pos):
    for button in BUTTONS:
        x, y, length, height = button['x'], button['y'], button['length'], button['height']
        pos_x, pos_y = pos
        if x <= pos_x <= x + length and y <= pos_y <= y + height:
            button['click']()


def random_maze_size():
    return random.randint(r1, r2) * 2 + 1
    # return random.randint(5, 20) * 2 + 1


def menu():
    global SOLVE_THREAD
    level = 0
    draw_menu()
    while not level:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
                    stop_thread(SOLVE_THREAD)
                    SOLVE_THREAD = None
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                dispatcher_click(mouse_pos)


if __name__ == '__main__':
    # menu
    menu()

    # game
    # size = random_maze_size()
    # MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    # SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    # SOLVE_THREAD.start()
    # while True:
    #     CLOCK.tick(FPS)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
    #                 stop_thread(SOLVE_THREAD)
    #                 SOLVE_THREAD = None
    #             exit(0)
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             mouse_pos = pygame.mouse.get_pos()
    #             dispatcher_click(mouse_pos)
