import logging

from auto_assistant.view.action_list_widgit import ActionListWidgit
from auto_assistant.view.add_action_dialog import AddActionDialog

logger = logging.getLogger(__name__)


def add_action(action_list_view: ActionListWidgit):
    dialog = AddActionDialog()
    logger.info('Opening the AddActionDialog')
    result = dialog.exec_()
    if result == 1:
        # Ok button was clicked (i.e. dialog was accepted)
        logger.info(f'AddActionDialog was {result}, the following action was created: {dialog.get_result()}')
        action_list_view.add_action(dialog.get_result())
    else:
        logger.info(f'User canceled adding an action, result was {result}')
