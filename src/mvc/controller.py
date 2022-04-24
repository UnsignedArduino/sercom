import logging
from typing import Union

from PyQt5.Qt import QKeyEvent
from PyQt5 import QtCore

from mvc.model import sercomModel
from mvc.view import sercomView
from utils.logger import create_logger
from utils.serial_config import NEWLINE_CR, NEWLINE_CRLF, \
    XON_XOFF_SOFT_FLOW_CONTROL, \
    RTS_CTS_HARD_FLOW_CONTROL, DSR_DTR_HARD_FLOW_CONTROL

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
        self.changed_serial_param()

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

    def set_baud_rate(self, rate: int):
        """
        Sets the baud rate.

        :param rate: An integer, can be custom or from utils/serial_config
        """
        logger.info(f"Setting baud rate to {rate}")
        self.model.port.baudrate = rate
        self.changed_serial_param()

    def set_byte_size(self, size: int):
        """
        Sets the byte size.

        :param size: An int, use the constants in utils/serial_config
        """
        logger.info(f"Setting byte size to {size}")
        self.model.port.bytesize = size
        self.changed_serial_param()

    def set_parity(self, parity: str):
        """
        Sets the parity.

        :param parity: A str, use the constants in utils/serial_config
        """
        logger.info(f"Setting parity to {parity}")
        self.model.port.parity = parity
        self.changed_serial_param()

    def set_stop_bits(self, stop_bits: Union[int, float]):
        """
        Sets the number of stop bits.

        :param stop_bits: An int or float, use the constants in
         utils/serial_config
        """
        logger.info(f"Setting stop bit count to {stop_bits}")
        self.model.port.stopbits = stop_bits
        self.changed_serial_param()

    def set_flow_control(self, control: int):
        """
        Set the flow control.

        :param control: An int, use the constants in utils/serial_config
        """
        self.model.port.xonxoff = False
        self.model.port.rtscts = False
        self.model.port.dsrdtr = False
        if control == XON_XOFF_SOFT_FLOW_CONTROL:
            logger.info("Enabling XON/XOFF (software) flow control")
            self.model.port.xonxoff = True
        elif control == RTS_CTS_HARD_FLOW_CONTROL:
            logger.info("Enabling RTS/CTS (hardware) flow control")
            self.model.port.rtscts = True
        elif control == DSR_DTR_HARD_FLOW_CONTROL:
            logger.info("Enabling DSR/DTR (hardware) flow control")
            self.model.port.dsrdtr = True
        self.changed_serial_param()

    def set_line_ending(self, ending: int):
        """
        Set the line ending.

        :param ending: An int, use the constants in utils/serial_config
        """
        logger.info(f"Setting line ending to {ending}")
        self.model.newline_mode = ending
        self.changed_serial_param()

    def changed_serial_param(self):
        """
        Emits a signal on the model that we changed serial params.
        """
        port = self.model.port
        notation = f"{port.bytesize}/{port.parity}/{port.stopbits}"
        notation += f" at {port.baudrate}"
        if port.xonxoff:
            notation += f" with XON/XOFF (soft)"
        elif port.rtscts:
            notation += f" with RTS/CTS (hard)"
        elif port.dsrdtr:
            notation += f" with DSR/DTR (hard)"
        else:
            notation += f" with no flow control"
        if self.model.newline_mode == NEWLINE_CRLF:
            notation += f" and \\r\\n ending"
        elif self.model.newline_mode == NEWLINE_CR:
            notation += f" and \\r ending"
        else:
            notation += f" and \\n ending"
        logger.debug(f"Serial port params: {notation}")
        self.model.serial_params_changed.emit(notation)

    def send_key(self, event: QKeyEvent):
        """
        Converts a key to a suitable byte sequence to send.

        :param event: The key event.
        """
        if ord(" ") <= event.key() <= ord("~"):
            self.model.send(event.text().encode())
        elif event.key() == QtCore.Qt.Key_Return:
            self.model.send((
                b"\n",
                b"\r",
                b"\r\n"
            )[self.model.newline_mode])
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.model.send(chr(8).encode())
