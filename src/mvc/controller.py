import logging

from mvc.model import sercomModel
from mvc.view import sercomView

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class sercomController:
    """
    sercom's controller where the view calls into the controller to call into
    the model, and the model returns results which are passed to the view.
    """

    def __init__(self, model: sercomModel, view: sercomView):
        """
        Initialize the controller.

        :param model: The model.
        :param view: The view.
        """
        logger.debug(f"Creating controller")
        self.model = model
        self.view = view
        self.model.controller = self
        self.view.controller = self
        self.model.after_controller_initialization()
        self.view.after_controller_initialization()

    def create_new_session(self):
        """
        "Forks" this process to create a new session that is independent of
        the current session.
        """
        logger.debug("Creating new session")
        self.model.create_new_session()

    def get_serial_ports(self) -> list[tuple[str, str]]:
        """
        Get the serial ports.
        """
        return self.model.get_serial_ports()

    def connect(self, path: str):
        """
        Attempts to connect to a serial port.

        :param path: The path, as a str. (ex. "COM8" on Windows)
        """
        self.model.connect(path)

    def disconnect(self):
        """
        Attempts to disconnect from the connected serial port.
        """
        self.model.disconnect()
