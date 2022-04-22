import logging

from PyQt5.QtCore import QObject
from serial.tools.list_ports import comports

from utils.logger import create_logger
from utils.process import launch_command, launch_detached

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

    def after_controller_initialization(self):
        """
        Stuff to run after the controller is initialized.
        """

    def create_new_session(self):
        """
        "Forks" this process to create a new session that is independent of
        the current session.
        """
        logger.debug("Creating new session")
        launch_detached(launch_command())

    def get_serial_ports(self) -> list[tuple[str, str]]:
        """
        Get the serial ports.
        """
        ports = []
        for port in comports():
            ports.append((port.device, f"{port.device} ({port.description})"))
        return ports
