#!/usr/bin/env python3

import logging
import sys

from pynput import mouse
from pynput.mouse import Button

log = logging.getLogger(__name__)


def on_click(x: int, y: int, button: mouse.Button, pressed):
    print(f'x is {type(x)}, y is {type(y)}, button is {type(button)}, pressed is {type(pressed)}')
    if pressed:
        print(f'Mouse was pressed at ({x}, {y}) with button {button}')
    else:
        print(f'Mouse was released at ({x}, {y}) with button {button}')


def main():
    log.info('Hello world')
    with mouse.Listener(
        on_click=on_click
    ) as listener:
        listener.join()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    main()
