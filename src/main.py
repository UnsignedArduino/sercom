import logging
import sys
from argparse import ArgumentParser, Namespace, ArgumentError
from time import time as unix
from traceback import format_exception

from PyQt5.QtWidgets import QApplication

from mvc.controller import sercomController
from mvc.model import sercomModel
from mvc.view import sercomView
from utils.dialogs import error_dlg
from utils.system_info import log_system_info
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

APPLICATION_NAME = "sercom"
APPLICATION_VERSION = "dev"
ORGANIZATION_NAME = "UnsignedArduino"


def process_my_args() -> tuple[Namespace, list[str]]:
    """
    Process the arguments for the application and leave the rest of the
    arguments for Qt.

    :return: A tuple of a Namespace and a list of strings for Qt.
    """
    parser = ArgumentParser(description="A serial monitor in Qt. ")
    # Add arguments here
    logger.debug(f"Parsing arguments")
    parsed, un_parsed = parser.parse_known_args()
    logger.debug(f"Application arguments parsed: {parsed}")
    logger.debug(f"Unparsed arguments: {un_parsed}")
    # Check/fix arguments here, and raise ArgumentError if needed
    logger.debug(f"Application arguments parsed after fixing: {parsed}")
    return parsed, un_parsed


def main():
    """
    The main function which is run when the program starts.
    """
    logger.debug(f"Starting application")

    start_time = unix()

    log_system_info()

    # https://stackoverflow.com/a/21166631/10291933
    parsed, un_parsed = process_my_args()
    qt_args = sys.argv[:1] + un_parsed

    app = QApplication(qt_args)

    try:
        logger.debug("Setting application ID for Windows")
        from ctypes import windll
        # mycompany.myproduct.subproduct.version
        # Company identifier use reverse-domain notation (com.mycompany)
        app_id = f"com.{ORGANIZATION_NAME}.{APPLICATION_NAME}.{APPLICATION_NAME}.{APPLICATION_VERSION}"
        logger.debug(f"Windows app ID: {app_id}")
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except ImportError:
        logger.exception("Failed to set application ID for Windows!")

    logger.debug("Setting application properties for Qt")
    QApplication.setApplicationName(APPLICATION_NAME)
    QApplication.setApplicationVersion(APPLICATION_VERSION)
    QApplication.setOrganizationName(ORGANIZATION_NAME)

    def error(cls, exception, traceback):
        """
        Except hook so we can actually see a traceback before exiting
        """
        sys.__excepthook__(cls, exception, traceback)
        error_dlg("sercom: Unhandled exception!",
                  "Unhandled exception, exiting!",
                  "".join(format_exception(cls, exception, traceback)))
        app.quit()

    # https://stackoverflow.com/a/33741755/10291933
    sys.excepthook = error

    model = sercomModel()

    view = sercomView()
    view.show()

    controller = sercomController(model, view)

    end_time = unix()
    startup_time = end_time - start_time

    logger.debug(f"Took {startup_time:.3f} seconds to initialize")

    logger.debug("Starting main loop")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
