import logging
import sys
from traceback import format_exception
from typing import Callable, Union, Optional, Any

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QMenu, QActionGroup, QFontDialog
from serial.serialutil import SerialException

from ui.autogenerated.main_window import Ui_main_window
from ui.wrappers.dialogs.enter_custom_port_dialog import EnterCustomPortDialog
from ui.wrappers.dialogs.set_baud_rate_dialog import SetBaudRateDialog
from utils.dialogs import error_dlg, confirm_dangerous_dlg
from utils.logger import create_logger
from utils.serial_config import \
    DEFAULT_BAUD_RATE, BYTE_SIZES, DEFAULT_BYTE_SIZE, \
    PARITIES, DEFAULT_PARITY, STOP_BITS, DEFAULT_STOP_BIT, \
    FLOW_CONTROLS, DEFAULT_FLOW_CONTROL, LINE_ENDINGS, DEFAULT_LINE_ENDING
from widgets.custom_plain_text_edit import CustomPlainTextEdit, \
    get_default_font

logger = create_logger(name=__name__, level=logging.DEBUG)


class sercomView(QMainWindow, Ui_main_window):
    """
    sercom's view where the GUI components are assembled.
    """

    def __init__(self):
        """
        Initialize the view.
        """
        logger.debug(f"Creating view")
        super().__init__()
        self.setupUi(self)
        self.text_edit = CustomPlainTextEdit()
        self.setCentralWidget(self.text_edit)
        self.create_configuration_menu()
        self.connect_signals()
        self.auto_scroll = True
        self.local_echo = False
        self.settings = QSettings()

    def connect_signals(self):
        """
        Connects the signals and slots together.
        """
        logger.debug("Connecting signals and slots")
        self.connect_signals_file_menu()
        self.connect_signals_port_menu()
        self.connect_signals_configuration_menu()
        self.connect_signals_view_menu()
        self.connect_signals_about_menu()

    def connect_signals_file_menu(self):
        """
        Connects the signals and slots together for the file menu.
        """
        self.action_new_session.triggered.connect(self.create_new_session)
        self.action_exit.triggered.connect(self.close)

    def connect_signals_port_menu(self):
        """
        Connects the signals and slots together for the port menu.
        """
        self.action_disconnect.triggered.connect(self.disconnect_from_port)

    def connect_signals_configuration_menu(self):
        """
        Connects the signals and slots together for the configuration menu.
        (that weren't already connected when making the menu)
        """
        self.action_baud_rate.triggered.connect(self.open_set_baud_rate_dialog)

    def connect_signals_view_menu(self):
        """
        Connects the signals and slots together for the view menu.
        """
        self.action_auto_scroll.toggled.connect(self.set_auto_scroll)
        self.action_local_echo.toggled.connect(self.set_local_echo)
        self.action_change_font.triggered.connect(self.change_font)

    def connect_signals_about_menu(self):
        """
        Connects the signals and slots together for the about menu.
        """
        self.action_reset_application.triggered.connect(self.maybe_reset_app)

    def update_serial_ports(self):
        """
        Updates the serial port listing in the "ports" menu.
        """
        self.menu_connect_to_port.clear()
        self.menu_connect_actions = []
        for path, name in self.controller.get_serial_ports():
            port_action = self.menu_connect_to_port.addAction(name)
            port_action.triggered.connect(
                lambda _, p=path: self.connect_to_port(p))
            tip = f"Connect to the serial port {path}"
            port_action.setStatusTip(tip)
            port_action.setToolTip(tip)
            self.menu_connect_actions.append(port_action)
        self.menu_connect_to_port.addSeparator()
        custom_port_action = self.menu_connect_to_port.addAction(
            "Enter &custom port...")
        custom_port_action.triggered.connect(self.enter_custom_port)
        tip = "Enter a custom port path to connect to. "
        custom_port_action.setStatusTip(tip)
        custom_port_action.setToolTip(tip)
        self.menu_connect_actions.append(custom_port_action)
        self.menu_connect_to_port.addSeparator()
        self.refresh_ports_action = self.menu_connect_to_port.addAction(
            "&Refresh port list...")
        self.refresh_ports_action.triggered.connect(self.update_serial_ports)
        tip = "Refresh the list of serial ports. "
        self.refresh_ports_action.setStatusTip(tip)
        self.refresh_ports_action.setToolTip(tip)
        self.menu_connect_actions.append(self.refresh_ports_action)

    def update_menu_states(self):
        """
        Updates the menu states.
        """
        connected = self.controller.model.connected
        for action in self.menu_connect_actions:
            if action != self.refresh_ports_action:
                action.setEnabled(not connected)
        self.action_disconnect.setEnabled(connected)

    def after_controller_initialization(self):
        """
        Stuff to run after the controller is initialized.
        """
        self.text_edit.controller = self.controller
        self.text_edit.after_controller_initialization()
        self.controller.model.received_text.connect(self.on_received_text)
        self.controller.model.local_echo_text.connect(self.on_local_echo)
        self.controller.model.disconnected.connect(self.disconnect_from_port)
        self.controller.model.serial_params_changed.connect(
            lambda n: self.action_serial_configuration.setText(n))
        self.update_serial_ports()
        self.update_menu_states()
        self.load_settings()

    def create_configuration_menu(self):
        """
        Create the configuration menu by hand, so we can make and attach event
        handlers to it.
        """

        def make_options(menu: QMenu, dictionary: dict[str, Union[str, int]],
                         default: Union[str, int],
                         tooltip: str, callback: Callable):
            """
            Make an action group and add it to a menu.

            :param menu: The menu to add to.
            :param dictionary: A dictionary of labels to actual values.
            :param default: The default value.
            :param tooltip: The tool tip format, with {thing} as the replace
             value.
            :param callback: A callback that will be passed in the key and
             value from dictionary.
            """
            group = QActionGroup(menu)
            group.setExclusive(True)
            for label, thing in dictionary.items():
                new_label = label
                if thing == default:
                    new_label += " (default)"
                action = menu.addAction(new_label)
                action.triggered.connect(
                    lambda _, t=thing,
                           l=label.replace("&", ""): callback(t, l))
                action.setCheckable(True)
                action.setChecked(thing == default)
                tip = tooltip.format(thing=label)
                action.setStatusTip(tip.replace("&", ""))
                action.setToolTip(tip.replace("&", ""))
                group.addAction(action)

        make_options(self.menu_byte_size, BYTE_SIZES, DEFAULT_BYTE_SIZE,
                     "Set the byte size to {thing}", self.set_byte_size)
        make_options(self.menu_parity, PARITIES, DEFAULT_PARITY,
                     "Set the parity to {thing}", self.set_parity)
        make_options(self.menu_stop_bits, STOP_BITS, DEFAULT_STOP_BIT,
                     "Set the number of stop bits to {thing}",
                     self.set_stop_bits)
        make_options(self.menu_flow_control, FLOW_CONTROLS,
                     DEFAULT_FLOW_CONTROL, "Set the flow control to {thing}",
                     self.set_flow_control)
        make_options(self.menu_line_ending, LINE_ENDINGS,
                     DEFAULT_LINE_ENDING, "Set the line ending sent and "
                                          "received to {thing}",
                     self.set_line_ending)

    def save_value(self, group: str, key: str, value: Any):
        """
        Saves the value in group.

        :param group: The group to save in.
        :param key: The key to save in.
        :param value: The value to save as.
        """
        logger.debug(f"Saving {group}/{key} as {value}")
        self.settings.beginGroup(group)
        self.settings.setValue(key, value)
        self.settings.endGroup()

    def load_value(self, key: str, default: Any,
                   func: Callable, convert_to: type):
        """
        If the key exists, then we will call the function with the result.

        :param key: The key name, as a string.
        :param default: The default value.
        :param func: The function, that accepts one value.
        :param convert_to: Converts the result of the function to that type.
        """
        logger.debug(f"Attempting to load key: {key}")
        if not self.settings.contains(key):
            logger.warning(f"Unable to find key {key}, setting default")
            self.settings.setValue(key, default)
        value = self.settings.value(key, type=convert_to)
        logger.debug(f"Key {key} = {value} (type: {convert_to})")
        func(value)

    def load_settings(self):
        self.settings.beginGroup("serial_port")
        self.load_value("baud_rate", DEFAULT_BAUD_RATE,
                        self.set_baud_rate, int)
        self.load_value("byte_size", DEFAULT_BYTE_SIZE,
                        self.set_byte_size, int)
        self.load_value("parity", DEFAULT_PARITY,
                        self.set_parity, str)
        self.load_value("stop_bits", DEFAULT_STOP_BIT,
                        self.set_stop_bits, float)
        self.load_value("flow_control", DEFAULT_FLOW_CONTROL,
                        self.set_flow_control, int)
        self.load_value("line_ending", DEFAULT_LINE_ENDING,
                        self.set_line_ending, int)
        self.settings.endGroup()
        self.settings.beginGroup("view")
        self.load_value("auto_scroll", True,
                        self.action_auto_scroll.setChecked, bool)
        self.load_value("local_echo", False,
                        self.action_local_echo.setChecked, bool)
        self.load_value("font", get_default_font(), self.set_font, QFont)
        self.settings.endGroup()

    def set_status(self, status: str):
        """
        Set the current status.

        :param status: A string.
        """
        self.status_bar.showMessage(f"{status}")

    def set_port_status(self, status: str):
        """
        Set the current port status. (Reflected in the port menu)

        :param status: A string.
        """
        self.action_port_status.setText(status)
        self.action_port_status.setToolTip(status)
        self.action_port_status.setStatusTip(status)

    def create_new_session(self):
        """
        "Forks" this process to create a new session that is independent of
        the current session.
        """
        logger.debug("Creating new session")
        self.set_status("Creating new session...")
        self.controller.create_new_session()
        self.set_status("Created new session.")

    def enter_custom_port(self):
        """
        Pops up a dialog to type a custom port, and try to connect if the user
        clicked ok.
        """
        logger.debug("Opening enter custom port dialog")
        self.set_status("Connecting to custom port...")
        success, name = EnterCustomPortDialog().exec()
        if success:
            logger.debug(f"Custom port entered: {name}")
            self.set_status(f"Connecting to custom port {name}...")
            self.connect_to_port(name)
        else:
            logger.debug("Canceled entering custom port")
            self.set_status("Canceled connecting to custom port.")

    def connect_to_port(self, port: str):
        """
        Connect to a port.

        :param port: The port to connect to.
        """
        self.set_status(f"Connecting to port {port}...")
        try:
            self.controller.connect(port)
        except SerialException as exc:
            self.set_status(f"Failed to connect to port {port}! ({exc})")
            self.set_port_status(f"Failed to connect to port {port}!")
            logger.exception(f"Failed to connect to port {port}!")
            error_dlg("sercom: Failed to connect to port!",
                      f"Failed to connect to port {port}!",
                      "".join(format_exception(*sys.exc_info())))
        else:
            self.set_status(f"Connected to port {port}!")
            self.set_port_status(f"Successfully connected to port {port}!")
            self.update_menu_states()
            self.text_edit.setPlaceholderText("Nothing was received.")
            self.setWindowTitle(f"sercom - {port}")

    def disconnect_from_port(self):
        """
        Disconnects from the connected port.
        """
        port = self.controller.model.port.name
        self.set_status(f"Disconnecting from port {port}...")
        self.set_port_status(f"Disconnected from port {port}.")
        self.controller.disconnect()
        self.set_status(f"Successfully disconnected from port {port}!")
        self.update_menu_states()
        self.text_edit.setPlaceholderText("Not connected to a port.")
        self.setWindowTitle(f"sercom")

    def open_set_baud_rate_dialog(self):
        """
        Opens the set baud rate dialog, and sets the baud rate if the users
        types in a baud rate.
        """
        logger.debug("Opening set baud rate dialog")
        self.set_status("Setting baud rate...")
        success, rate = SetBaudRateDialog().exec(
            self.controller.model.port.baudrate)
        if success:
            logger.debug(f"Baud rate entered: {rate}")
            self.set_baud_rate(rate)
        else:
            logger.debug("Canceled setting baud rate")
            self.set_status("Canceled setting baud rate.")

    def set_baud_rate(self, rate: int):
        """
        Sets the baud rate.

        :param rate: An integer.
        """
        self.set_status(f"Setting baud rate to {rate}...")
        self.controller.set_baud_rate(rate)
        self.set_status(f"Successfully set baud rate to {rate}!")
        self.save_value("serial_port", "baud_rate", rate)

    def set_byte_size(self, size: int, label: Optional[str] = None):
        """
        Sets the byte size.

        :param size: An int, use the constants in utils/serial_config
        :param label: The labeled value, optional.
        """
        if label is not None:
            self.set_status(f"Setting byte size to {label}...")
        self.controller.set_byte_size(size)
        if label is not None:
            self.set_status(f"Successfully set byte size to {label}!")
        self.save_value("serial_port", "byte_size", size)

    def set_parity(self, parity: str, label: Optional[str] = None):
        """
        Sets the parity.

        :param parity: A str, use the constants in utils/serial_config
        :param label: The labeled value, optional.
        """
        if label is not None:
            self.set_status(f"Setting parity to {label}...")
        self.controller.set_parity(parity)
        if label is not None:
            self.set_status(f"Successfully set parity to {label}!")
        self.save_value("serial_port", "parity", parity)

    def set_stop_bits(self, stop_bits: Union[int, float],
                      label: Optional[str] = None):
        """
        Sets the number of stop bits.

        :param stop_bits: An int or float, use the constants in
         utils/serial_config
        :param label: The labeled value, optional.
        """
        if label is not None:
            self.set_status(f"Setting number of stop bits to {label}...")
        if int(stop_bits) == stop_bits:
            stop_bits = int(stop_bits)
        self.controller.set_stop_bits(stop_bits)
        if label is not None:
            self.set_status(f"Successfully set number of "
                            f"stop bits to {label}!")
        self.save_value("serial_port", "stop_bits", stop_bits)

    def set_flow_control(self, control: int, label: Optional[str] = None):
        """
        Set the flow control.

        :param control: An int, use the constants in utils/serial_config
        :param label: The labeled value, optional.
        """
        if label is not None:
            self.set_status(f"Setting flow control to {label}...")
        self.controller.set_flow_control(control)
        if label is not None:
            self.set_status(f"Successfully set flow control to {label}!")
        self.save_value("serial_port", "flow_control", control)

    def set_line_ending(self, ending: int, label: Optional[str] = None):
        """
        Set the line ending.

        :param ending: An int, use the constants in utils/serial_config
        :param label: The labeled value, optional.
        """
        if label is not None:
            self.set_status(f"Setting line ending to {label}...")
        self.controller.set_line_ending(ending)
        if label is not None:
            self.set_status(f"Successfully set line ending to {label}!")
        self.save_value("serial_port", "line_ending", ending)

    def set_auto_scroll(self, do: bool):
        """
        Sets auto scroll.

        :param do: Whether to enable auto scroll or not.
        """
        self.auto_scroll = do
        logger.debug(f"Set auto scroll to {do}")
        if do:
            self.set_status("Enabled auto scroll.")
        else:
            self.set_status("Disabled auto scroll.")
        self.save_value("view", "auto_scroll", do)

    def set_local_echo(self, do: bool):
        """
        Sets local echo.

        :param do: Whether to enable local echo or not.
        """
        self.local_echo = do
        logger.debug(f"Set local echo to {do}")
        if do:
            self.set_status("Enabled local echo.")
        else:
            self.set_status("Disabled local echo.")
        self.save_value("view", "local_echo", do)

    def set_font(self, font: QFont):
        """
        Sets the text edit's current font.

        :param font: The new QFont.
        """
        display_name = f"{font.family()} {font.pointSize()}"
        for attr in ("bold", "italic", "underline", "strikeOut"):
            if getattr(font, attr)():
                display_name += f" {attr.lower()}"
        logger.debug(f"User selected font: {display_name}")
        self.text_edit.setFont(font)
        self.set_status(f"Successfully set font to {display_name}!")
        self.save_value("view", "font", font)

    def change_font(self):
        """
        Pops up a dialog to change the font.
        """
        logger.debug("Choosing font")
        font, success = QFontDialog.getFont(self.text_edit.font(),
                                            self,
                                            "sercom: Select a font",
                                            QFontDialog.MonospacedFonts)
        if success:
            self.set_font(font)
        else:
            logger.debug("User canceled selecting font")
            self.set_status("Canceled setting a font.")

    def reset_app(self):
        """
        Clears the application data to reset the app.
        """
        logger.warning("Clearing application data")
        self.set_status("Resetting application...")
        self.settings.clear()
        logger.info("Successfully cleared application data")
        self.set_status("Successfully reset application!")
        self.load_settings()

    def maybe_reset_app(self):
        """
        Pops up a dialog to confirm resetting the app.
        """
        logger.debug("Popping up confirm reset dialog")
        self.set_status("Confirming application reset...")
        if confirm_dangerous_dlg("sercom: Confirm application reset",
                                 "Are you sure you want to reset the "
                                 "application?"):
            self.reset_app()
        else:
            logger.debug("User canceled application reset.")
            self.set_status("Canceled application reset.")

    def on_received_text(self, data: bytes):
        """
        Callback when we receive text.

        :param data: The data received
        """
        self.text_edit.process_tty_data(data)
        if self.auto_scroll:
            self.text_edit.ensureCursorVisible()

    def on_local_echo(self, text: bytes):
        """
        Callback when we actually send data, for "local echo."

        :param text: A str.
        """
        if not self.local_echo:
            return
        self.on_received_text(text)
