# coding = utf-8
import threading

import pygame
from time import sleep

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
COLOR_DARK_BLUE = pygame.Color("#3F46CB")
COLOR_YELLOW = pygame.Color("#F1CA3A")

FONT_SIZE = 16
FONT = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE)
FONT_LARGE = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE * 3)

BUTTONS = []

SOLVE_THREAD = None

r1 = r2 = 0
level_select = ""

image = pygame.image.load('images/splash.jpg')
SCREEN.blit(image, (-79, 6))
pygame.display.update()
sleep(1)
pygame.mixer.init()
pygame.mixer.music.load('2.mp3')
pygame.mixer.music.play()


def draw_rect(x, y, len, color):
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)


def draw_back_button():
    image = pygame.image.load(".\\images\\back button.png")
    image = pygame.transform.scale(image, (15, 15))
    SCREEN.blit(image, [5, 7])


def draw_button(x, y, len, height, text):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(text, True, COLOR_DARK_BLUE)
    text_len = text.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


def draw_heading(x, y, len, text, color = COLOR_BLACK, font_size = FONT_SIZE):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT_LARGE.render(text, True, color)
    text_len = text.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len - 60) / 2, y + 5))

def draw_level_opener(x, y, len, height, text1, img, text2):
    # pygame.draw.rect(SCREEN, COLOR_YELLOW, [x, y, len, height], 1)
    text_surface = FONT.render(text1, True, COLOR_DARK_BLUE)
    text_len = text1.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x , y + 2))
    image = pygame.image.load(img)
    image = pygame.transform.scale(image, (int(len-3), int(len-3)))
    SCREEN.blit(image, [x,y+27])
    text_surface = FONT.render(text2, True, COLOR_DARK_BLUE)
    text_len = text1.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x , y + height - 30))


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
    SCREEN.fill(COLOR_WHITE)
    draw_heading(2, 2, WIDTH - 4, 'Maze', COLOR_DARK_BLUE, FONT_SIZE*3)

    # draw_button(2, 60, WIDTH - 4, HEADER - 4, 'Easy')
    # draw_button(2, 100, WIDTH - 4, HEADER - 4, 'Medium')
    # draw_button(2, 140, WIDTH - 4, HEADER - 4, 'Hard')

    draw_level_opener(0 * WIDTH/3 + 10, HEIGHT/2 - 75, WIDTH/3 - 10, WIDTH/3 + 50, "LEVEL 1", ".\\images\\easy.png", "Easy")
    draw_level_opener(1 * WIDTH/3 + 10, HEIGHT/2 - 75, WIDTH/3 - 10, WIDTH/3 + 50, "LEVEL 2", ".\\images\\medium.png", "Medium")
    draw_level_opener(2 * WIDTH/3 + 10, HEIGHT/2 - 75, WIDTH/3 - 10, WIDTH/3 + 50, "LEVEL 3", ".\\images\\hard.png", "Hard")

    # if len(BUTTONS) == 0:
    BUTTONS.append({
        'x': 0 * WIDTH/3 + 10,
        'y': HEIGHT/2 - 75,
        'length': WIDTH/3 - 10,
        'height': WIDTH/3 + 50,
        'click': easy
    })

    BUTTONS.append({
        'x': 1 * WIDTH/3 + 10,
        'y': HEIGHT/2 - 75,
        'length': WIDTH/3 - 10,
        'height': WIDTH/3 + 50,
        'click': medium
    })

    BUTTONS.append({
        'x': 2 * WIDTH/3 + 10,
        'y': HEIGHT/2 - 75,
        'length': WIDTH/3 - 10,
        'height':  WIDTH/3 + 50,
        'click': hard
    })

    pygame.display.flip()


def easy():
    global r1
    global r2
    global level_select
    r1 = 5
    r2 = 10
    level_select = "LEVEL 1 : Easy"
    refresh()


def medium():
    global r1
    global r2
    global level_select
    r1 = 10
    r2 = 15
    level_select = "LEVEL 2 : Medium"
    refresh()


def hard():
    global r1
    global r2
    global level_select
    r1 = 15
    r2 = 20
    level_select = "LEVEL 3 : Hard"
    refresh()


def draw_maze(maze, cur_pos, score):
    global level_select
    SCREEN.fill(COLOR_WHITE)
    draw_back_button()
    draw_button(30, 3, WIDTH - 150, HEADER - 4, level_select)
    draw_heading
    BUTTONS.clear()
    BUTTONS.append({
        'x': 2,
        'y': 2,
        'length': 24,
        'height': 25,
        'click': menu
    })
    BUTTONS.append({
        'x': 30,
        'y': 3,
        'length': WIDTH - 150,
        'height': HEADER - 4,
        'click': refresh
    })

    size = len(maze)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2
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
    draw_heading(1, HEIGHT - BOTTOM + 20, WIDTH // 3, str(score))
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
