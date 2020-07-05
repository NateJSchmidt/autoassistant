from auto_assistant.view.action_list_widgit import ActionListWidgit
from auto_assistant.view.add_action_dialog import AddActionDialog


def add_action(action_list_view: ActionListWidgit):
    dialog = AddActionDialog()
    result = dialog.exec_()
    print(f'dialog was {result}')
    if result == 1:
        print(f'action is {dialog.get_result()}')
        action_list_view.add_action(dialog.get_result())
