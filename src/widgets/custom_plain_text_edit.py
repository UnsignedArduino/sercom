import logging
import re
from codecs import getincrementaldecoder
from platform import system

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QFrame

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

# Copied from Mu at
# https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L143
VT100_RETURN = b"\r"
VT100_BACKSPACE = b"\b"
VT100_DELETE = b"\x1B[\x33\x7E"
VT100_UP = b"\x1B[A"
VT100_DOWN = b"\x1B[B"
VT100_RIGHT = b"\x1B[C"
VT100_LEFT = b"\x1B[D"
VT100_HOME = b"\x1B[H"
VT100_END = b"\x1B[F"


class CustomPlainTextEdit(QPlainTextEdit):
    """
    Our custom plain text edit.

    All thanks to Mu's MicroPythonREPLPane for making this possible:
    https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L154
    """

    def __init__(self):
        super().__init__()
        self.controller = None
        self.setObjectName("text_edit")
        self.setContextMenuPolicy(Qt.NoContextMenu)
        # self.setToolTip("The area where your serial data is sent and "
        #                 "received. ")
        # self.setStatusTip(self.toolTip())
        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setPlaceholderText("Not connected to a port.")
        # Copied from Mu at
        # https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L180
        self.device_cursor_pos = self.textCursor().position()
        self.decoder = getincrementaldecoder("utf8")("replace")
        self.vt100_regex = re.compile(
            r"\x1B\[(?P<count>[\d]*)(;?[\d]*)*(?P<action>[A-Za-z])"
        )
        self.unprocessed_input = b""

    def after_controller_initialization(self):
        """
        Stuff to run after the controller is initialized.
        """

    def keyPressEvent(self, e: QKeyEvent) -> None:
        """
        Handles the on key press event for the text edit.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L224
        """
        if not self.controller.model.connected:
            e.accept()
            return
        cursor = self.textCursor()
        key = e.key()
        ctrl_only_pressed = e.modifiers() == Qt.ControlModifier
        meta_only_pressed = e.modifiers() == Qt.MetaModifier
        ctrl_shift_only_pressed = e.modifiers() == \
                                  Qt.ControlModifier | Qt.ShiftModifier
        shift_pressed = e.modifiers() & Qt.ShiftModifier
        on_mac = system() == "Darwin"
        if key == Qt.Key_Return:
            cursor.movePosition(QTextCursor.End, mode=QTextCursor.MoveAnchor)
            self.device_cursor_pos = cursor.position()
            self.controller.send(VT100_RETURN)
        elif key == Qt.Key_Backspace:
            if not self.selection_deleted():
                self.controller.send(VT100_BACKSPACE)
        elif key == Qt.Key_Delete:
            if not self.selection_deleted():
                self.controller.send(VT100_DELETE)
        elif key == Qt.Key_Up:
            self.controller.send(VT100_UP)
        elif key == Qt.Key_Down:
            self.controller.send(VT100_DOWN)
        elif key == Qt.Key_Right:
            if shift_pressed:
                super().keyPressEvent(e)
            elif cursor.hasSelection():
                self.move_cursor_to(cursor.selectionEnd())
            else:
                self.controller.send(VT100_RIGHT)
        elif key == Qt.Key_Left:
            if shift_pressed:
                super().keyPressEvent(e)
            elif cursor.hasSelection():
                self.move_cursor_to(cursor.selectionStart())
            else:
                self.controller.send(VT100_LEFT)
        elif key == Qt.Key_Home:
            self.controller.send(VT100_HOME)
        elif key == Qt.Key_End:
            self.controller.send(VT100_END)
        elif (on_mac and meta_only_pressed) or \
             (not on_mac and ctrl_only_pressed):
            if Qt.Key_A <= key <= Qt.Key_Z:
                self.controller.send(bytes([1 + key - Qt.Key_A]))
        elif ctrl_shift_only_pressed or (on_mac and ctrl_only_pressed):
            if key == Qt.Key_C:
                self.copy()
            elif key == Qt.Key_V:
                self.selection_deleted()
                self.paste()
        else:
            self.selection_deleted()
            self.controller.send(bytes(e.text(), "utf-8"))
        # e.accept()

    def sync_our_cursor_to_device_cursor(self):
        """
        Resets the Qt TextCursor to where we know the device has the cursor
        placed.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L294
        """
        cursor = self.textCursor()
        cursor.setPosition(self.device_cursor_pos)
        self.setTextCursor(cursor)

    def sync_device_cursor_to_our_cursor(self):
        """
        Call this whenever the cursor has been moved by the user, to send
        the cursor movement to the device.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L303
        """
        self.move_cursor_to(self.textCursor().position())

    def move_cursor_to(self, new_pos: int):
        """
        Move the cursor, by sending VT100 left/right signals through serial.
        Our cursor is first returned to the known location
        of the device cursor. Then the appropriate number of move left or
        right signals are sent. Our is not moved to the new position here,
        but will be moved once receiving a response.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L310

        :param new_pos: An int.
        """
        self.sync_our_cursor_to_device_cursor()
        steps = new_pos - self.device_cursor_pos
        if steps > 0:
            self.controller.send(VT100_RIGHT * steps)
        elif steps < 0:
            self.controller.send(VT100_LEFT * abs(steps))

    def selection_deleted(self) -> bool:
        """
        Returns True if deletion happened, returns False if there was no
        selection to delete.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L330

        :return: A bool
        """
        cursor = self.textCursor()
        if cursor.hasSelection():
            size = cursor.selectionEnd() - cursor.selectionStart()
            self.move_cursor_to(cursor.selectionEnd())
            self.controller.send(VT100_BACKSPACE * size)
            return True
        else:
            return False

    def mouseReleaseEvent(self, e: QMouseEvent):
        """
        Called whenever a user have had a mouse button pressed, and
        releases it. We pass it through to the normal way Qt handles
        button pressed, but also sends as cursor movement signal to
        the device (except if a selection is made, for selections we first
        move the cursor on deselection)

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L346
        """
        super().mouseReleaseEvent(e)

        if not self.textCursor().hasSelection():
            self.sync_device_cursor_to_our_cursor()

    def process_tty_data(self, data: bytes):
        """
        Given some incoming bytes of data, work out how to handle / display
        them in the REPL widget.
        If received input is incomplete, stores remainder in
        self.unprocessed_input.
        Updates the self.device_cursor_position to match that of the device
        for every input received.

        Copied from Mu at
        https://github.com/mu-editor/mu/blob/9bc3e5cc7a480ea6a8084ed53ac135d5dc7b7167/mu/interface/panes.py#L360

        :param data: The data received.
        """
        i = 0
        data = self.decoder.decode(data)
        if len(self.unprocessed_input) > 0:
            data = self.unprocessed_input + data
            self.unprocessed_input = ""

        self.sync_our_cursor_to_device_cursor()
        cursor = self.textCursor()

        while i < len(data):
            if data[i] == "\b":
                cursor.movePosition(QTextCursor.Left)
                self.device_cursor_pos = cursor.position()
            # elif data[i] == "\r":
            #     # Carriage return. Do nothing, we handle newlines when
            #     # reading \n
            #     pass
            elif data[i] == "\x1b":
                # Escape
                if len(data) > i + 1 and data[i + 1] == "[":
                    # VT100 cursor detected: <Esc>[
                    match = self.vt100_regex.search(data[i:])
                    if match:
                        # move to (almost) after control seq
                        # (will ++ at end of loop)
                        i += match.end() - 1
                        count_string = match.group("count")
                        count = 1 if count_string == "" else int(count_string)
                        action = match.group("action")
                        if action == "A":  # up
                            cursor.movePosition(QTextCursor.Up, n=count)
                            self.device_cursor_pos = cursor.position()
                        elif action == "B":  # down
                            cursor.movePosition(QTextCursor.Down, n=count)
                            self.device_cursor_pos = cursor.position()
                        elif action == "C":  # right
                            cursor.movePosition(QTextCursor.Right, n=count)
                            self.device_cursor_pos = cursor.position()
                        elif action == "D":  # left
                            cursor.movePosition(QTextCursor.Left, n=count)
                            self.device_cursor_pos = cursor.position()
                        elif action == "K":  # delete things
                            if count_string == "":  # delete to end of line
                                cursor.movePosition(
                                    QTextCursor.EndOfLine,
                                    mode=QTextCursor.KeepAnchor,
                                )
                                cursor.removeSelectedText()
                                self.device_cursor_pos = cursor.position()
                        else:
                            # Unknown action, log warning and ignore
                            command = match.group(0).replace("\x1B", "<Esc>")
                            msg = "Received unsupported VT100 command: {}"
                            logger.warning(msg.format(command))
                    else:
                        # Cursor detected, but no match, must be
                        # incomplete input
                        self.unprocessed_input = data[i:]
                        break
                elif len(data) == i + 1:
                    # Escape received as end of transmission. Perhaps
                    # the transmission is incomplete, wait until next
                    # bytes are received to determine what to do
                    self.unprocessed_input = data[i:]
                    break
            elif data[i] == "\n":
                cursor.movePosition(QTextCursor.End)
                self.device_cursor_pos = cursor.position() + 1
                self.setTextCursor(cursor)
                self.insertPlainText(data[i])
            else:
                # Char received, with VT100 that should be interpreted
                # as overwrite the char in front of the cursor
                cursor.deleteChar()
                self.device_cursor_pos = cursor.position() + 1
                self.insertPlainText(data[i])
            self.setTextCursor(cursor)
            i += 1
        # # Scroll textarea if necessary to see cursor
        # self.ensureCursorVisible()
