# coding = utf-8
import sys
import os
import threading

import pygame
from time import sleep

from maze_generator import generate_maze
from maze_solver import solve_maze
from maze_solver import calc_time

# from maze_solver import AI
# from maze_solver import SCORE
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
COLOR_DARK_RED = (82, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_DARK_GREEN = (2, 100, 64)
COLOR_BLUE = (255, 160, 122)
COLOR_CYAN = (0, 255, 255)
COLOR_DARK_BLUE = pygame.Color("#3F46CB")
COLOR_YELLOW = pygame.Color("#F1CA3A")
COLOR_ORANGE = (255,165,0)
COLOR_DARK_ORANGE = (118,76,0)

FONT_SIZE = 16
FONT = pygame.font.Font("data/fonts/msyh.ttf", FONT_SIZE)
FONT_LARGE1 = pygame.font.Font("data/fonts/msyh.ttf", FONT_SIZE * 3)
FONT_LARGE2 = pygame.font.Font("data/fonts/msyh.ttf", int(FONT_SIZE * 1.5))

BUTTONS = []

SOLVE_THREAD = None
TIME_THREAD=None

r1 = r2 = 0
level_select = ""

# image = pygame.image.load('.\\data\\mazerr.jpg')
# SCREEN.blit(image, (-79, 6))
image = pygame.image.load('data/images/splash.jpg')
SCREEN.blit(image, (-79, 35))
pygame.display.update()
sleep(3)
pygame.mixer.init()
pygame.mixer.music.load('.\\data\\2.mp3')
pygame.mixer.music.play()

AI = False


def draw_rect(x, y, len, color):
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)


def draw_back_button():
    image = pygame.image.load(".\\data\\images\\back button.png")
    image = pygame.transform.scale(image, (15, 15))
    SCREEN.blit(image, [5, 7])


def draw_button(x, y, len, height, tdata, color=COLOR_DARK_BLUE):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(tdata, True, color)
    text_len = tdata.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


def draw_heading1(x, y, len, text, color=COLOR_BLACK, font_size=FONT_SIZE):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT_LARGE1.render(text, True, color)
    text_len = text.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x + (len - text_len - 60) / 2, y + 5))


def draw_heading2(x, y, len, text, color=COLOR_BLACK, font_size=FONT_SIZE):
    # pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT_LARGE2.render(text, True, color)
    text_len = text.__len__() * font_size
    SCREEN.blit(text_surface, (x + (len - text_len - 30) / 2, y))


def draw_level_opener(x, y, len, height, text1, img, text2):
    # pygame.draw.rect(SCREEN, COLOR_YELLOW, [x, y, len, height], 1)
    text_surface = FONT.render(text1, True, COLOR_DARK_BLUE)
    text_len = text1.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x, y + 2))
    image = pygame.image.load(img)
    image = pygame.transform.scale(image, (int(len - 3), int(len - 3)))
    SCREEN.blit(image, [x, y + 27])
    text_surface = FONT.render(text2, True, COLOR_DARK_BLUE)
    text_len = text1.__len__() * FONT_SIZE
    SCREEN.blit(text_surface, (x, y + height - 30))


def draw_end_screen(status, score):
    global SOLVE_THREAD,TIME_THREAD
    # print(SCORE)
    # SCORE = score
    # print(SCORE)
    # print(status, score)
    # if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
    #     stop_thread(SOLVE_THREAD)
    #     SOLVE_THREAD = None

    if TIME_THREAD is not None and TIME_THREAD.is_alive():
        stop_thread(TIME_THREAD)
        TIME_THREAD = None
    if status == 'complete':
        if AI :
            SCREEN.fill(COLOR_ORANGE)
            draw_heading1(80, 150, 200, "You Used AI", COLOR_DARK_ORANGE)
            draw_heading2(155, 225, 200, "To Complete the Level", COLOR_DARK_ORANGE)
            draw_button(25, 3, 20, 50, "Menu", COLOR_DARK_ORANGE)
            draw_button(380, 3, 20, 50, "Replay", COLOR_DARK_ORANGE)    
            pygame.display.update()

        else :
            SCREEN.fill(COLOR_GREEN)
            draw_heading1(85, 150, 200, "You Won", COLOR_DARK_GREEN)
            draw_heading2(150, 225, 200, "Congratulations", COLOR_DARK_GREEN)
            draw_heading2(150, 300, 200, "Your Score : " + str(score), COLOR_DARK_GREEN)
            draw_button(25, 3, 20, 50, "Menu", COLOR_DARK_GREEN)
            draw_button(380, 3, 20, 50, "Replay", COLOR_DARK_GREEN)
            pygame.display.update()

        # High Score update
        f = open("data/high_score.txt", "r")
        lines = f.read().splitlines()
        if r1 == 5 and score > int(lines[0]):
            lines[0] = str(score)
        if r1 == 10 and score > int(lines[1]):
            lines[1] = str(score)
        if r1 == 15 and score > int(lines[2]):
            lines[2] = str(score)
        f.close()
        f = open("data/high_score.txt", "w")
        f.write(lines[0] + '\n' + lines[1] + '\n' + lines[2])
        f.close()

    elif status == 'score_0':
        SCREEN.fill(COLOR_RED)
        draw_heading1(85, 150, 200, "You Lost", COLOR_DARK_RED)
        draw_heading2(150, 225, 200, "Better Luck Next Time", COLOR_DARK_RED)
        draw_heading2(150, 300, 200, "Your Score : " + str(score), COLOR_DARK_RED)
        draw_button(25, 3, 20, 50, "Menu", COLOR_DARK_RED)
        draw_button(380, 3, 20, 50, "Replay", COLOR_DARK_RED)
        pygame.display.update()


def refresh():
    global MAZE, SIZE, ENTRANCE, EXIT, SOLVE_THREAD, TIME_THREAD
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    SIZE = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(SIZE, SIZE)
    SOLVE_THREAD = threading.Thread(target=solve_maze,
                                    args=(MAZE, ENTRANCE, EXIT, draw_maze, draw_end_screen, display_time, AI))
    SOLVE_THREAD.start()

    # start_time = pygame.time.get_ticks()
    TIME_THREAD = threading.Thread(target=calc_time, args=(display_time,))
    TIME_THREAD.start()


def draw_menu():
    # check for high score file

    f = open("data/high_score.txt", "r+")
    lines = f.read().splitlines()
    if len(lines) == 0:
        f.write("0\n0\n0")
    f.close()

    SCREEN.fill(COLOR_WHITE)
    draw_heading1(2, 2, WIDTH - 4, 'Maze', COLOR_DARK_BLUE, FONT_SIZE * 3)

    # draw_button(2, 60, WIDTH - 4, HEADER - 4, 'Easy')
    # draw_button(2, 100, WIDTH - 4, HEADER - 4, 'Medium')
    # draw_button(2, 140, WIDTH - 4, HEADER - 4, 'Hard')

    draw_level_opener(0 * WIDTH / 3 + 10, HEIGHT / 2 - 75, WIDTH / 3 - 10, WIDTH / 3 + 50, "LEVEL 1",
                      ".\\data\\images\\easy.png", "Easy")
    draw_level_opener(1 * WIDTH / 3 + 10, HEIGHT / 2 - 75, WIDTH / 3 - 10, WIDTH / 3 + 50, "LEVEL 2",
                      ".\\data\\images\\medium.png", "Medium")
    draw_level_opener(2 * WIDTH / 3 + 10, HEIGHT / 2 - 75, WIDTH / 3 - 10, WIDTH / 3 + 50, "LEVEL 3",
                      ".\\data\\images\\hard.png", "Hard")

    # if len(BUTTONS) == 0:
    BUTTONS.append({
        'x': 0 * WIDTH / 3 + 10,
        'y': HEIGHT / 2 - 75,
        'length': WIDTH / 3 - 10,
        'height': WIDTH / 3 + 50,
        'click': easy
    })

    BUTTONS.append({
        'x': 1 * WIDTH / 3 + 10,
        'y': HEIGHT / 2 - 75,
        'length': WIDTH / 3 - 10,
        'height': WIDTH / 3 + 50,
        'click': medium
    })

    BUTTONS.append({
        'x': 2 * WIDTH / 3 + 10,
        'y': HEIGHT / 2 - 75,
        'length': WIDTH / 3 - 10,
        'height': WIDTH / 3 + 50,
        'click': hard
    })

    pygame.display.flip()


def easy():
    global r1
    global r2
    global level_select
    r1 = 5
    r2 = 7
    level_select = "LEVEL 1 : Easy"
    refresh()


def medium():
    global r1
    global r2
    global level_select
    r1 = 10
    r2 = 12
    level_select = "LEVEL 2 : Medium"
    refresh()


def hard():
    global r1
    global r2
    global level_select
    r1 = 15
    r2 = 17
    level_select = "LEVEL 3 : Hard"
    refresh()


def display_high_score():
    global r1
    f = open("data/high_score.txt", "r")
    lines = f.read().splitlines()
    if r1 == 5:  # Easy
        return lines[0]
    elif r1 == 10:  # Medium
        return lines[1]
    elif r1 == 15:  # Hard
        return lines[2]
    f.close()


def msec_to_time(msec):
    sec = msec // 100
    min, sec = divmod(sec, 60)
    min_str = ''
    sec_str = ''
    if min == 0:
        min_str = '00'
    elif min > 0 and min < 10:
        min_str = '0' + str(min)
    else:
        min_str = str(min)
    if sec == 0:
        sec_str = '00'
    elif sec > 0 and sec < 10:
        sec_str = '0' + str(sec)
    else:
        sec_str = str(sec)
    return min_str + ':' + sec_str


def display_time(curr_time,score):
    global SCREEN
    # draw_heading2(13 + WIDTH // 3, HEIGHT - BOTTOM + 20, WIDTH // 3, "       ")
    # pygame.display.flip()
    # draw_heading2(13 + WIDTH // 3, HEIGHT - BOTTOM + 20, WIDTH // 3, msec_to_time(curr_time))
    # pygame.draw.rect(SCREEN, COLOR_WHITE, [2+WIDTH//3,HEIGHT-BOTTOM , WIDTH//3, BOTTOM-4], 1)
    SCREEN.fill(COLOR_WHITE, (2, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4))
    draw_button(2, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, 'Score')
    draw_heading2(1, HEIGHT - BOTTOM + 20, WIDTH // 3, str(score))
    SCREEN.fill(COLOR_WHITE, (2 + WIDTH // 3, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4))
    draw_button(2 + WIDTH // 3, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, "Time")
    draw_heading2(13 + WIDTH // 3, HEIGHT - BOTTOM + 20, WIDTH // 3, msec_to_time(curr_time))
    pygame.display.flip()


def draw_maze(maze, cur_pos, score, time):
    global level_select
    SCREEN.fill(COLOR_WHITE)
    draw_back_button()
    draw_button(30, 3, WIDTH - 150, HEADER - 4, level_select)
    draw_button(200, 3, WIDTH - 150, HEADER - 4, "High Score : " + display_high_score())
    draw_button(380, 3, 20, HEADER - 4, "Replay")
    BUTTONS.clear()
    BUTTONS.append({
        'x': 2,
        'y': 2,
        'length': 40,
        'height': 25,
        'click': menu
    })
    BUTTONS.append({
        'x': 340,
        'y': 3,
        'length': 60,
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
    draw_heading2(1, HEIGHT - BOTTOM + 20, WIDTH // 3, str(score))
    # SCREEN.fill(COLOR_WHITE, (2 + WIDTH // 3, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4))
    #
    draw_button(2 + WIDTH // 3, HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, "Time")
    draw_heading2(13 + WIDTH // 3, HEIGHT - BOTTOM + 20, WIDTH // 3, msec_to_time(time))
    draw_button(2 + 2 * (WIDTH // 3), HEIGHT - BOTTOM, WIDTH // 3, BOTTOM - 4, 'AI')
    if (AI):
        draw_heading2(12 + 2 * (WIDTH // 3), HEIGHT - BOTTOM + 20, WIDTH // 3, 'ON')
    else:
        draw_heading2(12 + 2 * (WIDTH // 3), HEIGHT - BOTTOM + 20, WIDTH // 3, 'OFF')

    BUTTONS.append({
        'x': 2 + 2 * (WIDTH // 3),
        'y': HEIGHT - BOTTOM,
        'length': WIDTH // 3,
        'height': BOTTOM - 4,
        'click': ai_toggle,
        'arg1': maze,
        'arg2': cur_pos,
        'arg3': score,
        'arg4': display_time,

    })

    pygame.display.flip()


def ai_toggle():
    global AI, SOLVE_THREAD, SIZE
    AI = not AI
    # draw_maze(maze,cur_pos,score,display_time)
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    # size = random_maze_size()
    # MAZE, ENTRANCE, EXIT = generate_maze(SIZE, SIZE)

    # print(MAZE)
    for x in range(MAZE.__len__()):
        for y in range(MAZE.__len__()):
            if MAZE[x][y] != 1:
                MAZE[x][y] = 0
    SOLVE_THREAD = threading.Thread(target=solve_maze,
                                    args=(MAZE, ENTRANCE, EXIT, draw_maze, draw_end_screen, display_time, AI))
    SOLVE_THREAD.start()


def dispatcher_click(pos):
    for button in BUTTONS:
        x, y, length, height = button['x'], button['y'], button['length'], button['height']
        pos_x, pos_y = pos
        if x <= pos_x <= x + length and y <= pos_y <= y + height:
            # if button['click'] == ai_toggle:
            #     button['click'](button['arg1'], button['arg2'], button['arg3'], button['arg4'])
            # else:
            button['click']()


def random_maze_size():
    return random.randint(r1, r2) * 2 + 1
    # return random.randint(5, 20) * 2 + 1


def menu():
    global SOLVE_THREAD, TIME_THREAD
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None

    if TIME_THREAD is not None and TIME_THREAD.is_alive():
        stop_thread(TIME_THREAD)
        TIME_THREAD = None
    level = 0
    draw_menu()
    while not level:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
                    stop_thread(SOLVE_THREAD)
                    SOLVE_THREAD = None

                if TIME_THREAD is not None and TIME_THREAD.is_alive():
                    stop_thread(TIME_THREAD)
                    TIME_THREAD = None
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
