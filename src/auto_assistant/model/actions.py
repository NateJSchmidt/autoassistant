import abc
import enum
import logging

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

    def execute(self) -> None:
        # TODO - we need to actually implement this
        print(f'Going to click at ({self.__x}, {self.__y})')
        logger.error('Unimplement method: ClickAction.execute')

    def __str__(self):
        return f'Click at ({self.__x}, {self.__y})'

    def get_action_type(self) -> ActionType:
        return ActionType.CLICK_ACTION


class SleepAction(Action):
    def __init__(self, time_in_secs: int):
        self.__time_secs = time_in_secs

    def execute(self) -> None:
        # TODO - we need to actually implement this
        logger.error('Unimplemented method: SleepAction.execute')

    def __str__(self):
        return f'Sleep for {self.__time_secs}s'

    def get_action_type(self) -> ActionType:
        return ActionType.SLEEP_ACTION


class ActionListModel:
    def __init__(self):
        self.__list_of_actions = []

    def add_action(self, action: Action):
        logger.info(f'Adding the following action to our ActionListModel: {action}')
        self.__list_of_actions.append(action)
        logger.info(f'Total actions in model: {len(self.__list_of_actions)}')
