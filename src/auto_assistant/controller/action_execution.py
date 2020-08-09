import logging
import time
import threading
import typing

from auto_assistant.model.actions import ActionListModel

logger = logging.getLogger(__name__)


class Engine:
    def __init__(self, list_of_actions: ActionListModel, execution_finished_callback: typing.Callable[[None], None]):
        self.__is_executing = False
        self.__actions = list_of_actions
        self.__my_thread = None
        self.__callback = execution_finished_callback

    def start_execution(self):
        logger.info(f'Starting execution on {self.__actions.get_number_of_actions()} actions')
        self.__is_executing = True
        self.__my_thread = threading.Thread(target=self.__execute)
        self.__my_thread.start()

    def stop_execution(self):
        if self.__is_executing:
            logger.info('Stopping execution')
            self.__is_executing = False
            self.__my_thread.join()
        self.__callback()

    def __execute(self):
        for action in self.__actions:
            # TODO - for testing
            time.sleep(3)

            # before executing each action, make sure the user hasn't stopped execution
            if self.__is_executing:
                logger.info(f'Executing action: {action}')
                action.execute()
            else:
                break
        if self.__is_executing:
            logger.info(f'Finished execution')
        else:
            logger.info('User manually stopped execution')
        self.__is_executing = False
        self.__callback()
