import typing

from auto_assistant.model.actions import Action, ActionListModel
from PySide2 import QtWidgets


class ActionListWidgit(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.__action_list_model = ActionListModel()

    def add_action(self, action: Action):
        self.__action_list_model.add_action(action)
        widgit_item = QtWidgets.QListWidgetItem(str(action), self)

    def get_model(self) -> ActionListModel:
        return self.__action_list_model
