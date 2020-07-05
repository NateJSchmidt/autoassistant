import sys

from PySide2 import QtWidgets, QtGui

from auto_assistant.controller import actions_controller
from auto_assistant.view import action_list_widgit


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__configure_menu_bar()
        self.__configure_layout()
        self.resize(800, 600)

    def __configure_layout(self):
        top_widgit = QtWidgets.QWidget()
        top_grid = QtWidgets.QGridLayout()

        button_bar = QtWidgets.QGridLayout()
        add_action_button = QtWidgets.QPushButton('Add action')
        self.__edit_action_button = QtWidgets.QPushButton('Edit action')
        self.__edit_action_button.setEnabled(False)
        button_bar.addWidget(add_action_button, 0, 0)
        button_bar.addWidget(self.__edit_action_button, 0, 1)
        top_grid.addLayout(button_bar, 0, 0)

        self.__action_list_view = action_list_widgit.ActionListWidgit()
        top_grid.addWidget(self.__action_list_view, 1, 0)

        top_widgit.setLayout(top_grid)
        self.setCentralWidget(top_widgit)

        # connect up the button functionality
        print(f'action list is {self.__action_list_view}')
        add_action_button.clicked.connect(
            lambda: actions_controller.add_action(self.__action_list_view))

    def __configure_menu_bar(self):
        self.my_menu_bar = self.menuBar()
        self.file_menu = self.my_menu_bar.addMenu('File')

        self.exit_action = self.file_menu.addAction('Exit')
        self.exit_action.triggered.connect(self.close)
        self.exit_action.setShortcut(QtGui.QKeySequence('Ctrl+q'))

    def closeEvent(self, event: QtGui.QCloseEvent):
        print(f'Closing the window due to event: {event}')


def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    return app.exec_()


if __name__ == '__main__':
    main()
