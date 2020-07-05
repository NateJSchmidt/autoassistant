import abc


class Action(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None:
        pass

    @abc.abstractmethod
    def __str__(self):
        return ""


class ClickAction(Action):
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def execute(self) -> None:
        # TODO - we need to actually implement this
        print(f'Going to click at ({self.__x}, {self.__y})')

    def __str__(self):
        return f'Click at ({self.__x}, {self.__y})'


class ActionListModel:
    def __init__(self):
        self.__list_of_actions = []

    def add_action(self, action: Action):
        self.__list_of_actions.append(action)
        print(f'Total actions in model: {len(self.__list_of_actions)}')
