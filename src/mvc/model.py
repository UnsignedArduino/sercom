import logging

from PyQt5.QtCore import QObject, pyqtSignal

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class sercomModel(QObject):
    """
    sercom's model where the real image manipulation happens.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        logger.debug(f"Creating model")
        super().__init__()
