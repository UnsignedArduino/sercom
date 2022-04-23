import logging
import platform

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def log_system_info():
    """
    Log system information from the platform module.
    """
    platform_things = (
        "architecture",
        "machine",
        "node",
        "platform",
        "processor",
        "python_build",
        "python_compiler",
        "python_branch",
        "python_implementation",
        "python_revision",
        "python_version",
        "release",
        "system",
        "version",
        "java_ver",
        "win32_ver",
        "win32_edition",
        "win32_is_iot",
        "mac_ver",
        "libc_ver",
        "freedesktop_os_release"
    )
    logger.debug("Getting system information")
    for thing in platform_things:
        if hasattr(platform, thing):
            logger.debug(f"{thing}: "
                         f"{getattr(platform, thing)()}")
        else:
            logger.debug(f"{thing}: could not obtain")
