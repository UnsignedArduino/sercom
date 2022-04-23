import logging
from typing import Optional

from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ui.autogenerated.dialogs.set_baud_rate_dialog import Ui_baud_rate_dialog
from utils.logger import create_logger
from utils.serial_config import ALL_BAUD_RATES, DEFAULT_BAUD_RATE

logger = create_logger(name=__name__, level=logging.DEBUG)


class SetBaudRateDialog(QDialog, Ui_baud_rate_dialog):
    """
    The set baud rate dialog box.
    """

    def __init__(self):
        """
        Initialize the dialog.
        """
        logger.debug("Creating set baud rate dialog")
        super().__init__()
        self.setupUi(self)
        for rate in ALL_BAUD_RATES:
            if rate == DEFAULT_BAUD_RATE:
                self.baud_rate_combobox.addItem(f"{rate} (default)")
            else:
                self.baud_rate_combobox.addItem(f"{rate}")
        self.update_button_box()
        self.connect_signals()

    def connect_signals(self):
        """
        Connects all the signals and slots together.
        """
        self.baud_rate_combobox.currentTextChanged.connect(self.update_button_box)

    def update_button_box(self):
        """
        Update the button box - enables if we have typed in a custom port,
        otherwise Ok option is disabled.
        """
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(
            len(self.baud_rate_combobox.currentText()) > 0 and
            self.baud_rate_combobox.currentText().isnumeric() and
            int(self.baud_rate_combobox.currentText()) > 0
        )

    def exec(self, cur_rate: int) -> tuple[bool, Optional[int]]:
        """
        Pops the dialog up, and returns when the dialog is closed, either via
        the button box or the X button.

        :param cur_rate: The current baud rate, as an integer.
        :return: A tuple of 2 elements - the first object is a bool, which is
         True if the user clicked ok, otherwise False. The second object is an
         int of the new baud rate if the user clicked ok, otherwise it is None.
        """
        if cur_rate == DEFAULT_BAUD_RATE:
            self.baud_rate_combobox.setCurrentText(f"{cur_rate} (default)")
        else:
            self.baud_rate_combobox.setCurrentText(str(cur_rate))
        if super().exec() == 1:
            cur_text = self.baud_rate_combobox.currentText()
            return True, int(cur_text.split(" ")[0])
        else:
            return False, None
