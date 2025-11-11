import sys
import random
import time
import os
from pynput.keyboard import Key, Listener


def show():
    os.system('cls' if os.name == 'nt' else 'clear')

    header = f"Points: {points} | Press ESC to quit"

    matrix_content = '\n'.join([' '.join(map(str, row)) for row in matrix])

    print(f"{header}\n{matrix_content}")

def is_there_space(matrix):
    for row in matrix:
        for item in row:
            if item == ' ' or item == '@':
                return True
    return False


def fruit(matrix):
    fruitX = random.randint(1, 9)  # Change from 11 to 9
    fruitY = random.randint(1, 11)  # Change from 9 to 11
    while matrix[fruitX][fruitY] != ' ':
        fruitX = random.randint(1, 9)
        fruitY = random.randint(1, 11)
    fruit_pos = [fruitX, fruitY]
    matrix[fruit_pos[0]][fruit_pos[1]] = '@'
    return matrix

def show_time(start, end):
    duration = end - start
    min = int(duration // 60)
    sec = int(duration % 60)
    time_played = f"{min}m {sec}s"
    print(f"Time played: {time_played}")


def on_press(key):
    global direction

    key_map = {
        Key.up: 'up',
        Key.down: 'down',
        Key.left: 'left',
        Key.right: 'right'
    }

    try:
        new_dir = key_map.get(key)

        if new_dir:
            if (new_dir == 'up' and direction != 'down') or \
                    (new_dir == 'down' and direction != 'up') or \
                    (new_dir == 'left' and direction != 'right') or \
                    (new_dir == 'right' and direction != 'left'):
                direction = new_dir

    except AttributeError:
        if key == Key.esc:
            global game_over
            game_over = True
            return False

listener = Listener(on_press=on_press)
listener.start()

matrix = [
        ['|', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
        ['|', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '|']
    ]

snake_body = [[5, 6]]
matrix[snake_body[0][0]][snake_body[0][1]] = '#'
points = 0
start = time.time()

fruit(matrix)
show()
direction = 'right'
game_over = False
game_speed = 0.2

while is_there_space(matrix) and not game_over:

    new_head = list(snake_body[0])

    match direction:
        case 'up':
            new_head[0] = new_head[0] - 1
        case 'down':
            new_head[0] = new_head[0] + 1
        case 'left':
            new_head[1] = new_head[1] - 1
        case 'right':
            new_head[1] = new_head[1] + 1
        case _:
            pass

    next_cell = matrix[new_head[0]][new_head[1]]

    if next_cell in ['|', '-', '#']:
        print('\nYou died! Play again (Wall or Self Collision)!')
        game_over = True
        end = time.time()
        print('Points: ', points)
        show_time(start, end)
        break

    eats_fruit = False
    if next_cell == '@':
        eats_fruit = True
        fruit(matrix)
        points = points + 10

    snake_body.insert(0, new_head)

    if not eats_fruit:
        tail = snake_body.pop()
        matrix[tail[0]][tail[1]] = ' '

    for segment in snake_body:
        matrix[segment[0]][segment[1]] = '#'

    show()
    time.sleep(game_speed)

end = time.time()

listener.stop()
listener.join()

if not game_over:
    print("Congratulations! You won!")
    print(f"Points: {points}")
    show_time(start, end)
    sys.exit()