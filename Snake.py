import sys
import random
import time
import os
from pynput.keyboard import Key, Listener
from colorama import init, Cursor, Style, Fore, Back

init()

matrix = [
    ['|', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
    ['|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|'],
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
direction = 'right'
game_over = False
game_speed = 0.2


def print_at_pos(x, y, text):
    sys.stdout.write(Cursor.POS(x, y) + text)
    sys.stdout.flush()


def print_board_once():
    os.system('cls' if os.name == 'nt' else 'clear')

    for i, row in enumerate(matrix):
        print_at_pos(1, i + 3, ' '.join(map(str, row)))


def show_header():
    header = f"{Fore.CYAN}Points: {points}{Style.RESET_ALL} | Press {Fore.RED}ESC{Style.RESET_ALL} to quit"
    print_at_pos(1, 1, header)


def update_moving_parts(new_head, old_body_segment, tail, eats_fruit):

    if tail:
        print_at_pos(tail[1] * 2 + 1, tail[0] + 3, ' ')

    if old_body_segment:
        print_at_pos(old_body_segment[1] * 2 + 1, old_body_segment[0] + 3, f'{Fore.GREEN}#{Style.RESET_ALL}')

    print_at_pos(new_head[1] * 2 + 1, new_head[0] + 3, f'{Fore.MAGENTA + Style.BRIGHT}#{Style.RESET_ALL}')

    if eats_fruit:
        for r, row in enumerate(matrix):
            for c, cell in enumerate(row):
                if cell == '@':
                    print_at_pos(c * 2 + 1, r + 3, f'{Fore.YELLOW}@{Style.RESET_ALL}')
                    return


def is_there_space(matrix):
    for row in matrix:
        for item in row:
            if item == ' ' or item == '@':
                return True
    return False


def fruit(matrix):
    fruitX = random.randint(1, 9)
    fruitY = random.randint(1, 11)
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

print_board_once()
show_header()
fruit(matrix)
update_moving_parts(snake_body[0], None, None, True)

while is_there_space(matrix) and not game_over:

    old_head_pos = list(snake_body[0])
    new_head = list(snake_body[0])
    tail = None

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
        game_over = True
        end = time.time()
        print_at_pos(1, len(matrix) + 4, f'{Fore.RED}\nYou died! Play again!{Style.RESET_ALL}')
        print(f'\nPoints: {points}')
        show_time(start, end)
        break

    eats_fruit = False
    if next_cell == '@':
        eats_fruit = True
        fruit(matrix)
        points = points + 10

    matrix[new_head[0]][new_head[1]] = '#'
    snake_body.insert(0, new_head)

    if not eats_fruit:
        tail = snake_body.pop()
        matrix[tail[0]][tail[1]] = ' '


    old_body_segment = old_head_pos if len(snake_body) > 1 else None
    update_moving_parts(new_head, old_body_segment, tail, eats_fruit)

    show_header()

    time.sleep(game_speed)

end = time.time()
listener.stop()
listener.join()

if not game_over:
    print_at_pos(1, len(matrix) + 4, f"{Fore.GREEN}Congratulations! You won!{Style.RESET_ALL}")
    print(f"Points: {points}")
    show_time(start, end)
    sys.exit()

print('\n\n')
