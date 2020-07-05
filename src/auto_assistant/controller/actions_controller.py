from auto_assistant.view.action_list_widgit import ActionListWidgit
from auto_assistant.view.add_action_dialog import AddActionDialog


def add_action(action_list_view: ActionListWidgit):
    dialog = AddActionDialog()
    result = dialog.exec_()
    if result == 1:
        # Ok button was clicked (i.e. dialog was accepted)
        action_list_view.add_action(dialog.get_result())
