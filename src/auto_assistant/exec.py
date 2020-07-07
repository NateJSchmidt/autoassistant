#!/usr/bin/env python3

import argparse
import logging
import sys

from auto_assistant.view.main_window import MainWindow

from PySide2 import QtWidgets

log = logging.getLogger(__name__)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    return app.exec_()


class FilterOutWarnAndHigher(logging.Filter):
    def filter(self, record: logging.LogRecord) -> int:
        if record.levelno >= logging.WARNING:
            return 0
        else:
            return 1


class FilterOutLessThanWarn(logging.Filter):
    def filter(self, record: logging.LogRecord) -> int:
        if record.levelno < logging.WARNING:
            return 0
        else:
            return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode (turn on console logging)')
    args = vars(parser.parse_args())
    logger = logging.getLogger()
    formatter = logging.Formatter(fmt='%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - [%(levelname)s]: %(message)s')
    if args['debug']:
        logger.setLevel(logging.NOTSET)
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.addFilter(FilterOutWarnAndHigher())
        handler_stdout.setFormatter(formatter)
        handler_stderr = logging.StreamHandler(sys.stderr)
        handler_stderr.addFilter(FilterOutLessThanWarn())
        handler_stderr.setFormatter(formatter)
        logger.addHandler(handler_stderr)
        logger.addHandler(handler_stdout)
    else:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('autoassistant.log', mode='w')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    main()
