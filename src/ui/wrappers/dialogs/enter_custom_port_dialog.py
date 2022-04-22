import logging
from typing import Optional

from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ui.autogenerated.dialogs.enter_custom_port_dialog import \
    Ui_custom_port_dialog
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class EnterCustomPortDialog(QDialog, Ui_custom_port_dialog):
    """
    The enter custom port dialog box.
    """

    def __init__(self):
        """
        Initialize the dialog.
        """
        logger.debug("Creating enter custom port dialog")
        super().__init__()
        self.setupUi(self)
        self.update_button_box()
        self.connect_signals()

    def connect_signals(self):
        """
        Connects all the signals and slots together.
        """
        self.custom_port_lineedit.textChanged.connect(self.update_button_box)

    def update_button_box(self):
        """
        Update the button box - enables if we have typed in a custom port,
        otherwise Ok option is disabled.
        """
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(
            len(self.custom_port_lineedit.text()) > 0
        )

    def exec(self) -> tuple[bool, Optional[str]]:
        """
        Pops the dialog up, and returns when the dialog is closed, either via
        the button box or the X button.

        :return: A tuple of 2 elements - the first object is a bool, which is
         True if the user clicked ok, otherwise False. The second object is a
         string of the port if the user clicked
         ok, otherwise it is None.
        """
        selected = super().exec() == 1
        return selected, self.custom_port_lineedit.text() if selected else None
