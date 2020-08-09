import sys

from PySide2 import QtWidgets, QtGui

from auto_assistant.controller import actions_controller, action_execution
from auto_assistant.view import action_list_widgit


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__configure_menu_bar()
        self.__configure_layout()
        self.__engine = action_execution.Engine(self.__action_list_view.get_model(),
                                                self._engine_execution_finished_callback)
        self.resize(800, 600)

    def __configure_layout(self):
        top_widgit = QtWidgets.QWidget()
        top_grid = QtWidgets.QGridLayout()

        button_bar = QtWidgets.QGridLayout()
        self.__add_action_button = QtWidgets.QPushButton('Add action')
        self.__edit_action_button = QtWidgets.QPushButton('Edit action')
        self.__edit_action_button.setEnabled(False)
        button_bar.addWidget(self.__add_action_button, 0, 0)
        button_bar.addWidget(self.__edit_action_button, 0, 1)
        top_grid.addLayout(button_bar, 0, 0)

        self.__action_list_view = action_list_widgit.ActionListWidgit()
        top_grid.addWidget(self.__action_list_view, 1, 0)

        execution_bar = QtWidgets.QGridLayout()
        self.__start_execution_button = QtWidgets.QPushButton('Start')
        self.__stop_execution_button = QtWidgets.QPushButton('Stop')
        self.__stop_execution_button.setEnabled(False)
        execution_bar.addWidget(self.__start_execution_button, 0, 0)
        execution_bar.addWidget(self.__stop_execution_button, 0, 1)
        top_grid.addLayout(execution_bar, 2, 0)

        top_widgit.setLayout(top_grid)
        self.setCentralWidget(top_widgit)

        # connect up the button functionality
        print(f'action list is {self.__action_list_view}')
        self.__add_action_button.clicked.connect(
            lambda: actions_controller.add_action(self.__action_list_view))
        self.__start_execution_button.clicked.connect(self.__execute_actions)
        self.__stop_execution_button.clicked.connect(self.__stop_action_execution)

    def toggle_buttons(self, is_executing: bool):
        if is_executing:
            self.__add_action_button.setEnabled(False)
            self.__edit_action_button.setEnabled(False)
            self.__start_execution_button.setEnabled(False)
            self.__stop_execution_button.setEnabled(True)
        else:
            self.__add_action_button.setEnabled(True)
            self.__edit_action_button.setEnabled(True)
            self.__start_execution_button.setEnabled(True)
            self.__stop_execution_button.setEnabled(False)

    def __execute_actions(self):
        # configure the buttons for execution (only let the stop button be clickable)
        self.toggle_buttons(True)
        self.__engine.start_execution()

    def __stop_action_execution(self):
        # configure the buttons for non-execution (only disable the stop button)
        self.__engine.stop_execution()
        self.toggle_buttons(False)

    def __configure_menu_bar(self):
        self.my_menu_bar = self.menuBar()
        self.file_menu = self.my_menu_bar.addMenu('File')

        self.exit_action = self.file_menu.addAction('Exit')
        self.exit_action.triggered.connect(self.close)
        self.exit_action.setShortcut(QtGui.QKeySequence('Ctrl+q'))

    def closeEvent(self, event: QtGui.QCloseEvent):
        print(f'Closing the window due to event: {event}')

    def _engine_execution_finished_callback(self):
        self.toggle_buttons(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    return app.exec_()


if __name__ == '__main__':
    main()
