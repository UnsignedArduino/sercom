import logging
from subprocess import Popen, DEVNULL, STDOUT
from sys import argv, executable
from time import time as unix

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def launch_command() -> list[str]:
    """
    Returns the command used to run the current process.

    :return: A list of strings which is the command. .
    """
    cmd = [executable] + argv
    logger.debug(f"Launch commands: {cmd}")
    return cmd


def launch_detached(cmd: list[str], silenced: bool = True):
    """
    Run a command detached.

    :param cmd: The command to run, as a list of strings.
    :param silenced: Whether to run the command silenced. Defaults to True.
    """
    logger.debug(f"Running detached command: {cmd}")

    start_time = unix()
    # https://stackoverflow.com/a/34459371/10291933
    if silenced:
        Popen(cmd, close_fds=True, stdout=DEVNULL, stderr=STDOUT)
    else:
        Popen(cmd, close_fds=True)

    end_time = unix()
    launch_time = end_time - start_time
    logger.debug(f"Took {launch_time:.3f} seconds to launch detached process")
