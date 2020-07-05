from auto_assistant.model import actions

from pynput import mouse
from PySide2 import QtWidgets


class AddActionDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.__result = None
        my_layout = QtWidgets.QGridLayout()

        button_grid = QtWidgets.QGridLayout()
        self.__ok_button = QtWidgets.QPushButton('Ok')
        self.__cancel_button = QtWidgets.QPushButton('Cancel')
        button_grid.addWidget(self.__cancel_button, 0, 0)
        button_grid.addWidget(self.__ok_button, 0, 1)
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        input_grid = QtWidgets.QGridLayout()
        x_label = QtWidgets.QLabel('x: ')
        self.__x_value = QtWidgets.QLabel('1')
        y_label = QtWidgets.QLabel('y: ')
        self.__y_value = QtWidgets.QLabel('1')
        input_grid.addWidget(x_label, 0, 0)
        input_grid.addWidget(self.__x_value, 0, 1)
        input_grid.addWidget(y_label, 0, 2)
        input_grid.addWidget(self.__y_value, 0, 3)
        get_click_button = QtWidgets.QPushButton('Get click')
        input_grid.addWidget(get_click_button, 1, 0, 1, -1)

        my_layout.addLayout(input_grid, 0, 0)
        my_layout.addLayout(button_grid, 1, 0)
        self.setLayout(my_layout)

        self.__mouse_listener = mouse.Listener(on_click=self.__on_click)

        # hook up the button to get the click
        get_click_button.clicked.connect(self.__get_click)

    def __toggle_buttons_to(self, enabled: bool):
        self.__ok_button.setEnabled(enabled)
        self.__cancel_button.setEnabled(enabled)

    def __get_click(self):
        self.__mouse_listener.start()
        self.__toggle_buttons_to(False)

    def __on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> bool:
        # print(f'Clicked at ({x}, {y}) with button {button} and pressed={pressed}')
        if pressed and button == mouse.Button.left:
            self.__x_value.setText(str(x))
            self.__y_value.setText(str(y))
            self.__toggle_buttons_to(True)

            # reset the mouse listener for next time
            self.__mouse_listener = mouse.Listener(on_click=self.__on_click)
        return False

    def get_result(self) -> actions.Action:
        return self.__result

    def accept(self):
        super().accept()
        print('Accepting')
        self.__result = actions.ClickAction(int(self.__x_value.text()), int(self.__y_value.text()))

    def reject(self):
        super().reject()
        print('Rejecting')
