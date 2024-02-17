#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import argparse
import threading
import RPi.GPIO as GPIO
import random
import os

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT

lft_input = 16
rht_input = 20
up_input = 12
dwn_input = 21
rst_input = 13
mid_input = 6

GPIO.setmode(GPIO.BCM)  # zet pin mode
GPIO.setup(lft_input, GPIO.IN)
GPIO.setup(rht_input, GPIO.IN)
GPIO.setup(up_input, GPIO.IN)
GPIO.setup(dwn_input, GPIO.IN)
GPIO.setup(rst_input, GPIO.IN)
GPIO.setup(mid_input, GPIO.IN)


def demo(w, h, block_orientation, rotate):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=w, height=h, rotate=rotate, block_orientation=block_orientation)
    print("Created device")

    def loss():
        msg = 'You lost :('
        show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

    def won():
        msg = 'You won! X'
        show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
        time.sleep(1)
        msg = 'X'
        show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

    def no_win():
        msg = 'no one won :/'
        show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)

    def check_for_win(board):
        for idx, line in enumerate(board):
            if board[idx][0] == board[idx][1] and board[idx][1] == board[idx][2] and board[idx][1] != '-':
                print(f'Player {board[idx][1]} won!')
                if board[idx][1] == 'x':
                    print('win 1a')
                    return 'win'
                elif board[idx][1] == 'o':
                    print('win 1b')
                    return 'loss'

            elif board[0][idx] == board[1][idx] and board[1][idx] == board[2][idx] and board[1][idx] != '-':
                print(f'Player {board[1][idx]} won!')
                print(f'{board[0][idx]} = {board[1][idx]} & {board[1][idx]} = {board[2][idx]}')
                if board[1][idx] == 'x':
                    print('win 2a')
                    return 'win'
                elif board[1][idx] == 'o':
                    print('win 2b')
                    return 'loss'

            elif board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != '-':
                print(f'Player {board[1][1]} won!')
                if board[1][1] == 'x':
                    print('win 3a')
                    return 'win'
                elif board[1][1] == 'o':
                    print('win 3b')
                    return 'loss'

            elif board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[1][1] != '-':
                print(f'Player {board[1][1]} won!')
                if board[1][1] == 'x':
                    print('win 4a')
                    return 'win'
                elif board[1][1] == 'o':
                    print('win 4b')
                    return 'loss'

        row_score = 0

        for row in board:
            item = '-'
            if item in row:
                return None
            else:
                row_score += 1
                if row_score == 3:
                    print('No one won :(')
                    return 'equal'

    def update_board_visual(board):
        for y_idx, y_pos in enumerate(board):
            row = []
            for x_pos in board[y_idx]:
                row.append(x_pos)
            print(f'\t{row[0]} {row[1]} {row[2]}')

    def manual_update():
        with canvas(device) as draw:
            print(valux)
            draw.rectangle((int(valux), int(valuy), int(valux) + 3, int(valuy) + 3), outline='white')

            gridy1 = 0
            gridy2 = 1

            for idxy, ycor in enumerate(grid):

                gridx1 = 0
                gridx2 = 1
                for idxx, xcor in enumerate(grid[idxy]):
                    if grid[idxy][idxx] == 'x':

                        draw.rectangle((int(gridx1), int(gridy1), int(gridx2), int(gridy2)), fill='white')
                        # draw.point((int(gridx2), int(gridy2)), fill='white')
                        # print(f'{gridx1} {gridy1} - {gridx2} {gridy2}')
                    elif grid[idxy][idxx] == 'o':

                        draw.line((int(gridx1), int(gridy1), int(gridx2), int(gridy2)), fill='white')
                        # draw.point((int(gridx2), int(gridy2)), fill='white')
                        # print(f'{gridx1} {gridy1} - {gridx2} {gridy2}')

                    gridx1 += 3
                    gridx2 += 3

                gridy1 += 3
                gridy2 += 3

        time.sleep(.5)

    entered = True
    valux = 2
    valuy = 2

    grid = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]

    lost = False

    while True:
        if entered:
            with canvas(device) as draw:
                print(valux)
                draw.rectangle((int(valux), int(valuy), int(valux)+3, int(valuy)+3), outline='white')

                gridy1 = 0
                gridy2 = 1

                for idxy, ycor in enumerate(grid):

                    gridx1 = 0
                    gridx2 = 1
                    for idxx, xcor in enumerate(grid[idxy]):
                        if grid[idxy][idxx] == 'x':

                            draw.rectangle((int(gridx1), int(gridy1), int(gridx2), int(gridy2)), fill='white')
                            # draw.point((int(gridx2), int(gridy2)), fill='white')
                            # print(f'{gridx1} {gridy1} - {gridx2} {gridy2}')
                        elif grid[idxy][idxx] == 'o':

                            draw.line((int(gridx1), int(gridy1), int(gridx2), int(gridy2)), fill='white')
                            # draw.point((int(gridx2), int(gridy2)), fill='white')
                            # print(f'{gridx1} {gridy1} - {gridx2} {gridy2}')

                        gridx1 += 3
                        gridx2 += 3

                    gridy1 += 3
                    gridy2 += 3

            time.sleep(.5)
        entered = False

        board = grid

        def ai_time():
            # PLAYER AI
            print('player o [AI]')
            choice_y = random.randint(0, 2)
            choice_x = random.randint(0, 2)

            if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                time.sleep(.1)
                print(f'enter xcor: {choice_y}')
                time.sleep(.1)
                print(f'enter ycor: {choice_x}')

                board[int(choice_x)][int(choice_y)] = 'o'
            else:
                option = False
                while not option:
                    choice_y = random.randint(0, 2)
                    choice_x = random.randint(0, 2)
                    if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                        time.sleep(.1)
                        print(f'enter xcor: {choice_y}')
                        time.sleep(.1)
                        print(f'enter ycor: {choice_x}')

                        option = True
                        board[int(choice_x)][int(choice_y)] = 'o'

            update_board_visual(board)

            if check_for_win(board) == 'loss':
                loss()
                time.sleep(2)
                return 'lost'
            elif check_for_win(board) == 'equal':
                no_win()
                time.sleep(2)
                return 0
            else:
                pass


        if GPIO.input(lft_input) == 1:
            entered = True
            valux += 3
        elif GPIO.input(rht_input) == 1:
            entered = True
            valux -= 3
        elif GPIO.input(up_input) == 1:
            entered = True
            valuy += 3
        elif GPIO.input(dwn_input) == 1:
            entered = True
            valuy -= 3
        elif GPIO.input(rst_input) == 1:
            msg = 'Bye!'
            show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
            os.system('sudo shutdown now -h')
            exit(0)
        elif GPIO.input(mid_input) == 1:
            entered = True
            board = grid

            for y_idx, y_pos in enumerate(board):
                row = []
                for x_pos in board[y_idx]:
                    row.append(x_pos)
                print(f'\t{row[0]} {row[1]} {row[2]}')

            # PLAYER 1
            if valux == -1:
                choice_y = 0
            elif valux == 2:
                choice_y = 1
            elif valux == 5:
                choice_y = 2

            if valuy == -1:
                choice_x = 0
            elif valuy == 2:
                choice_x = 1
            elif valuy == 5:
                choice_x = 2
            print(f'width height\n'
                  f'{choice_x} {choice_y}\n'
                  f'{valuy} {valux}')
            if board[int(choice_x)][int(choice_y)] != 'x' and board[int(choice_x)][int(choice_y)] != 'o':
                board[int(choice_x)][int(choice_y)] = 'x'
            else:
                option = False
                if not option:
                    print('This spot has already been chosen')
                    pass

            update_board_visual(board)
            manual_update()

            if check_for_win(board) == 'win':
                won()
                time.sleep(2)
                return 0
            elif check_for_win(board) == 'equal':
                no_win()
                time.sleep(2)
                return 0
            else:
                pass

            grid = board

            restart = ai_time()
            if restart == 'lost':
                return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--width', type=int, default=8, help='Width')
    parser.add_argument('--height', type=int, default=8, help='height')
    parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90],
                        help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=3, choices=[0, 1, 2, 3], help='Rotation factor')

    args = parser.parse_args()
    while True:
        print('starting new game')
        try:
            demo(args.width, args.height, args.block_orientation, args.rotate)
        except KeyboardInterrupt:
            pass
