import abc
import enum
import logging
import time

from pynput.mouse import Controller, Button

logger = logging.getLogger(__name__)


@enum.unique
class ActionType(enum.Enum):
    CLICK_ACTION = 'Click action'
    SLEEP_ACTION = 'Sleep action'


class Action(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None:
        pass

    @abc.abstractmethod
    def __str__(self):
        return ""

    @abc.abstractmethod
    def get_action_type(self) -> ActionType:
        pass


class ClickAction(Action):
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__mouse_controller = Controller()

    def execute(self) -> None:
        logger.info(f'Going to click at ({self.__x}, {self.__y}).  Current position is '
                    f'{self.__mouse_controller.position}')

        # first save off the current mouse position to put it back
        current_position = self.__mouse_controller.position

        # move the mouse and click
        self.__mouse_controller.position = (self.__x, self.__y)
        logger.info('Mouse moved')
        time.sleep(.100)
        self.__mouse_controller.click(Button.left)

        # move the mouse back
        self.__mouse_controller.position = current_position
        logger.info(f'Done clicking at ({self.__x}, {self.__y})')

    def __str__(self):
        return f'Click at ({self.__x}, {self.__y})'

    def get_action_type(self) -> ActionType:
        return ActionType.CLICK_ACTION


class SleepAction(Action):
    def __init__(self, time_in_secs: float):
        self.__time_secs = time_in_secs

    def execute(self) -> None:
        logger.info(f'Sleeping for {self.__time_secs} seconds')
        time.sleep(self.__time_secs)
        logger.info(f'Done sleeping for {self.__time_secs} seconds')

    def __str__(self):
        return f'Sleep for {self.__time_secs}s'

    def get_action_type(self) -> ActionType:
        return ActionType.SLEEP_ACTION


class ActionListModel:
    def __init__(self):
        self.__list_of_actions = []

    def __len__(self):
        return len(self.__list_of_actions)

    def __iter__(self):
        return iter(self.__list_of_actions)

    def add_action(self, action: Action):
        logger.info(f'Adding the following action to our ActionListModel: {action}')
        self.__list_of_actions.append(action)
        logger.info(f'Total actions in model: {len(self.__list_of_actions)}')

    def get_number_of_actions(self) -> int:
        return len(self.__list_of_actions)
