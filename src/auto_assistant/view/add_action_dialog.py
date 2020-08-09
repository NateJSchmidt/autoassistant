import logging

from PySide2 import QtWidgets, QtGui, QtCore
from pynput import mouse

from auto_assistant.model import actions

logger = logging.getLogger(__name__)
_SECONDS_IN_A_DAY = 86400


class AddActionDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.__result = None
        self.__my_layout = QtWidgets.QGridLayout()

        button_grid = QtWidgets.QGridLayout()
        self.__ok_button = QtWidgets.QPushButton('Ok')
        self.__cancel_button = QtWidgets.QPushButton('Cancel')
        button_grid.addWidget(self.__cancel_button, 0, 0)
        button_grid.addWidget(self.__ok_button, 0, 1)
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        pick_action_combo_box = QtWidgets.QComboBox()
        pick_action_combo_box.addItems([i.value for i in actions.ActionType])
        pick_action_combo_box.currentTextChanged.connect(self.__handle_action_type_change)

        # The default type of grid will be one for a ClickAction
        self.__input_grid = self.__generate_grid_layout_for_click_action()

        self.__my_layout.addWidget(pick_action_combo_box, 0, 0)
        self.__my_layout.addLayout(self.__input_grid, 1, 0)
        self.__my_layout.addLayout(button_grid, 2, 0)
        self.setLayout(self.__my_layout)

    def __clear_items_in(self, layout: QtWidgets.QLayout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if isinstance(item, QtWidgets.QLayout):
                self.__clear_items_in(item)
            else:
                logger.debug(f'Removing {type(item.widget())}')
                item.widget().deleteLater()
        logger.debug(f'Removing {type(layout)}')
        layout.deleteLater()

    def __handle_action_type_change(self, selected_action_type: str):
        logger.info(f'Generating UI for {selected_action_type}')
        if self.__input_grid is not None:
            self.__my_layout.removeItem(self.__input_grid)
            self.__clear_items_in(self.__input_grid)
            self.__input_grid = None
            logger.info('\tOld UI removed')
        try:
            self.__input_grid = self.__generate_grid_layout_for(actions.ActionType(selected_action_type))
            self.__my_layout.addLayout(self.__input_grid, 1, 0)
        except RuntimeError:
            logger.error('Unable to generate the input grid', exc_info=True)

    def __generate_grid_layout_for(self, action_type: actions.ActionType) -> QtWidgets.QGridLayout:
        if actions.ActionType.CLICK_ACTION == action_type:
            return self.__generate_grid_layout_for_click_action()
        elif actions.ActionType.SLEEP_ACTION == action_type:
            return self.__generate_grid_layout_for_sleep_action()
        else:
            raise RuntimeError(f'Unsupported action type: {action_type}')

    def __generate_grid_layout_for_sleep_action(self) -> QtWidgets.QGridLayout:
        self.__ok_button.setEnabled(True)
        return_value = QtWidgets.QGridLayout()

        # create the label
        duration_label = QtWidgets.QLabel('Sleep for (secs): ')
        duration_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return_value.addWidget(duration_label, 0, 0)

        # create the input for the time
        self.__sleep_text_line = QtWidgets.QLineEdit()
        self.__sleep_text_line.setPlaceholderText('Enter time in seconds')
        self.__sleep_text_line.setValidator(QtGui.QIntValidator(0, _SECONDS_IN_A_DAY))
        self.__sleep_text_line.editingFinished.connect(self.__handle_sleep_time_input)
        return_value.addWidget(self.__sleep_text_line, 0, 1)

        return return_value

    def __handle_sleep_time_input(self):
        self.__result = actions.SleepAction(int(self.__sleep_text_line.text()))

    def __generate_grid_layout_for_click_action(self) -> QtWidgets.QGridLayout:
        self.__ok_button.setEnabled(False)
        return_value = QtWidgets.QGridLayout()
        x_label = QtWidgets.QLabel('x: ')
        x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.__x_value = QtWidgets.QLabel('1')
        y_label = QtWidgets.QLabel('y: ')
        y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.__y_value = QtWidgets.QLabel('1')
        return_value.addWidget(x_label, 0, 0)
        return_value.addWidget(self.__x_value, 0, 1)
        return_value.addWidget(y_label, 0, 2)
        return_value.addWidget(self.__y_value, 0, 3)
        self.__get_click_button = QtWidgets.QPushButton('Get click')
        self.__get_click_button.clicked.connect(self.__get_click)
        self.__mouse_listener = mouse.Listener(on_click=self.__on_click)
        return_value.addWidget(self.__get_click_button, 1, 0, 1, -1)
        return return_value

    def __toggle_buttons_to(self, enabled: bool):
        self.__ok_button.setEnabled(enabled)
        self.__cancel_button.setEnabled(enabled)
        self.__get_click_button.setEnabled(enabled)

    def __get_click(self):
        self.__mouse_listener.start()
        self.__toggle_buttons_to(False)

    def __on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> bool:
        logger.debug(f'Clicked at ({x}, {y}) with button {button} and pressed={pressed}')
        if pressed and button == mouse.Button.left:
            self.__x_value.setText(str(x))
            self.__y_value.setText(str(y))
            self.__toggle_buttons_to(True)

            # reset the mouse listener for next time
            self.__mouse_listener = mouse.Listener(on_click=self.__on_click)
            self.__result = actions.ClickAction(int(self.__x_value.text()), int(self.__y_value.text()))
        return False

    def get_result(self) -> actions.Action:
        return self.__result

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()
        self.__result = None
