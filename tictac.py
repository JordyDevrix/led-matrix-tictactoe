import random
import time


def check_for_win(board):
    for idx, line in enumerate(board):
        if board[idx][0] == board[idx][1] and board[idx][1] == board[idx][2] and board[idx][1] != '-':
            print(f'Player {board[idx][1]} won!')
            return False

        elif board[0][idx] == board[1][idx] and board[1][idx] == board[2][idx] and board[1][idx] != '-':
            print(f'Player {board[1][idx]} won!')
            return False

        elif board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != '-':
            print(f'Player {board[1][1]} won!')
            return False

        elif board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[1][1] != '-':
            print(f'Player {board[1][1]} won!')
            return False

    row_score = 0

    for row in board:
        item = '-'
        if item in row:
            return True
        else:
            row_score += 1
            if row_score == 3:
                print('No one won :(')
                return False


def update_board_visual(board):
    for y_idx, y_pos in enumerate(board):
        row = []
        for x_pos in board[y_idx]:
            row.append(x_pos)
        print(f'\t{row[0]} {row[1]} {row[2]}')


def play():
    board = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]

    for y_idx, y_pos in enumerate(board):
        row = []
        for x_pos in board[y_idx]:
            row.append(x_pos)
        print(f'\t{row[0]} {row[1]} {row[2]}')

    running = True
    first = 0
    four_positions = [[0, 0], [0, 2], [2, 2], [2, 0]]
    while running:
        # AI PLAYER MEDIUM
        print('player o [AI]')
        if first == 0:
            first += 1
            choice_y = 1
            choice_x = 1
        elif first == 1:
            position = random.choice(four_positions)
            choice_y = position[0]
            choice_x = position[1]
            print(position)
            first += 1
        else:
            choice_y = random.randint(0, 2)
            choice_x = random.randint(0, 2)

        if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
            time.sleep(1)
            print(f'enter xcor: {choice_y}')
            time.sleep(.3)
            print(f'enter ycor: {choice_x}')

            board[int(choice_x)][int(choice_y)] = 'o'
        elif first == 2:
            option = False
            while not option:
                position = random.choice(four_positions)
                choice_y = position[0]
                choice_x = position[1]
                if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                    time.sleep(1)
                    print(f'enter xcor: {choice_y}')
                    time.sleep(.3)
                    print(f'enter ycor: {choice_x}')

                    option = True
                    board[int(choice_x)][int(choice_y)] = 'o'
        else:
            option = False
            while not option:
                choice_y = random.randint(0, 2)
                choice_x = random.randint(0, 2)
                if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                    time.sleep(1)
                    print(f'enter xcor: {choice_y}')
                    time.sleep(.3)
                    print(f'enter ycor: {choice_x}')

                    option = True
                    board[int(choice_x)][int(choice_y)] = 'o'

        update_board_visual(board)

        if not check_for_win(board):
            running = False
            continue

        # PLAYER 1
        print('player x')
        choice_y = int(input('enter xcor: '))
        choice_x = int(input('enter ycor: '))

        if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
            board[int(choice_x)][int(choice_y)] = 'x'
        else:
            option = False
            while not option:
                print('This spot has already been chosen')
                choice_y = int(input('enter xcor: '))
                choice_x = int(input('enter ycor: '))
                if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                    option = True
                    board[int(choice_x)][int(choice_y)] = 'x'

        update_board_visual(board)

        if not check_for_win(board):
            running = False
            continue
