#!/usr/bin/env python3

import argparse
import logging
import sys

from pynput import mouse

exit_flag = False
log = logging.getLogger(__name__)


def on_click(x: int, y: int, button: mouse.Button, pressed) -> bool:
    log.info(f'x is {type(x)}, y is {type(y)}, button is {type(button)}, pressed is {type(pressed)}')
    if pressed:
        log.info(f'Mouse was pressed at ({x}, {y}) with button {button}')
    else:
        log.info(f'Mouse was released at ({x}, {y}) with button {button}')

    if exit_flag:
        return False
    else:
        return True


def display_option_menu():
    print('Please enter a command')
    print('[c] Create a new macro')
    print('[x] Quit')


def display_create_options():
    print('Please pick one of the following types of steps')


def main():
    global exit_flag
    log.info('Hello world')
    # listener = mouse.Listener(on_click=on_click)
    # listener.start()
    while not exit_flag:
        display_option_menu()
        user_input = input()
        print(f'You entered: {user_input}')
        if 'x' == user_input.lower():
            exit_flag = True
        elif 'c' == user_input.lower():
            display_create_options()

    print('leaving main')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode (turn on console logging)')
    args = vars(parser.parse_args())
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if args['debug']:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler('autoassistant.log')
    logger.addHandler(handler)
    main()
    print('leaving program')
