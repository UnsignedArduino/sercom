from typing import Optional

from PyQt5.QtWidgets import QMessageBox


def make_dlg(title: str, text: str,
             details: Optional[str] = None) -> QMessageBox:
    """
    Make a dialog and set the title, text, and details. Does not show the
    dialog!

    :param title: The title of the dialog.
    :param text: The text of the dialog.
    :param details: The details of the dialog. Pass None to show none.
    :return: The QMessageBox.
    """
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.setDetailedText(details)
    return dlg


def error_dlg(title: str, text: str, details: Optional[str] = None):
    """
    Pops up an error dialog.

    :param title: The title of the dialog.
    :param text: The text of the dialog.
    :param details: The details of the dialog. Pass None to show none.
    """
    dlg = make_dlg(title, text, details)
    dlg.setIcon(QMessageBox.Critical)
    dlg.setStandardButtons(QMessageBox.Ok)
    dlg.buttonClicked.connect(dlg.close)
    dlg.exec()
