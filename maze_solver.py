import time

# from maze import AI

AI = False
SCORE = 1000


class CellType:
    ROAD = 0
    WALL = 1
    WALKED = 2
    DEAD = 3


class Direction:
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3,


def valid(maze, x, y):
    if x < 0 or y < 0:
        return False
    if x >= len(maze) or y >= len(maze):
        return False
    val = maze[y][x]
    if val == CellType.WALL:
        return False
    return val, x, y


def neighbors(maze, pos):
    x, y = pos
    t, r, d, l = valid(maze, x, y - 1), valid(maze, x + 1, y), valid(maze, x, y + 1), valid(maze, x - 1, y)
    return t, r, d, l


def mark_walked(maze, pos):
    maze[pos[1]][pos[0]] = CellType.WALKED


def mark_dead(maze, pos):
    maze[pos[1]][pos[0]] = CellType.DEAD


def suggest_pos(cells):
    if not AI:
        time.sleep(50)

    arr = []
    for cell in cells:
        if cell:
            # if cell[0] == CellType.DEAD:
            arr.append(cell[0])
        else:
            arr.append(CellType.DEAD)
    if arr[1] == CellType.ROAD:
        return cells[1]
    if arr[2] == CellType.ROAD:
        return cells[2]
    return cells[arr.index(min(arr))]


def suggest_pos_man(cells):
    import pygame
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if cells[0]:
                return cells[0]
        if keys[pygame.K_RIGHT]:
            if cells[1]:
                return cells[1]
        if keys[pygame.K_DOWN]:
            if cells[2]:
                return cells[2]
        if keys[pygame.K_LEFT]:
            if cells[3]:
                return cells[3]


def solve_maze(maze, pos, end, callback):
    global SCORE
    time.sleep(0.1)
    if pos[0] == end[0] and pos[1] == end[1]:
        mark_walked(maze, pos)
        return True
    t, r, d, l = neighbors(maze, pos)
    if not AI:
        if pos[0] == 0:
            next_pos = r
        else:
            next_pos = suggest_pos_man((t, r, d, l))
    else:
        next_pos = suggest_pos((t, r, d, l))
    if next_pos:
        if next_pos[0] == CellType.WALKED:
            mark_dead(maze, pos)
            SCORE -= 5
        else:
            SCORE -= 1
            mark_walked(maze, pos)
        callback(maze, next_pos,SCORE)
        return solve_maze(maze, (next_pos[1], next_pos[2]), end, callback)
    else:
        mark_dead(maze, pos)
        callback(maze, next_pos)
        return False
