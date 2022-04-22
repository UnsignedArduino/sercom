import logging

from PyQt5.QtCore import QObject
from serial import Serial
from serial.tools.list_ports import comports

from utils.logger import create_logger
from utils.process import launch_command, launch_detached

logger = create_logger(name=__name__, level=logging.DEBUG)


class sercomModel(QObject):
    """
    sercom's model is where the serial port stuff happens.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        logger.debug(f"Creating model")
        super().__init__()
        self.port = Serial()

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

    def connect(self, path: str):
        """
        Attempts to connect to a serial port.

        :param path: The path, as a str. (ex. "COM8" on Windows)
        """
        logger.debug(f"Attempting to connect to port {path}")
        self.port = Serial(path)
        logger.info(f"Successfully connect to port {self.port.name}!")

    @property
    def connected(self) -> bool:
        """
        Returns whether we are connected to a serial port or not.

        :return: A boolean.
        """
        return self.port.is_open

    def disconnect(self):
        """
        Attempts to disconnect from the connected serial port.
        """
        port = self.port.name
        logger.debug(f"Attempting to disconnect from port {port}")
        self.port.close()
        logger.info(f"Successfully disconnected from port {port}!")
