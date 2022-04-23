import logging
from platform import system

from serial import *
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


# COMMON_BAUD_RATES = (
#     50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200,
#     38400, 57600, 115200
# )

COMMON_BAUD_RATES = Serial.BAUDRATES
logger.debug(f"Ccommon baud rates available: {COMMON_BAUD_RATES}")

HIGH_SPEED_BAUD_RATES = (
    230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000,
    2500000, 3000000, 3500000, 4000000
)
logger.debug(f"High speed baud rates: {HIGH_SPEED_BAUD_RATES}")

ALL_BAUD_RATES = COMMON_BAUD_RATES + HIGH_SPEED_BAUD_RATES

DEFAULT_BAUD_RATE = 9600
logger.debug(f"Default baud rate: {DEFAULT_BAUD_RATE}")

# BYTE_SIZES = {
#     "&5 bits": FIVEBITS,
#     "&6 bits": SIXBITS,
#     "&7 bits": SEVENBITS,
#     "&8 bits": EIGHTBITS
# }
BYTE_SIZES = dict(zip(
    (f"&{s} bits" for s in Serial.BYTESIZES),
    Serial.BYTESIZES
))
logger.debug(f"Byte sizes available: {BYTE_SIZES}")

DEFAULT_BYTE_SIZE = EIGHTBITS
logger.debug(f"Default byte size: {DEFAULT_BYTE_SIZE}")

# PARITIES = {
#     "&No parity": PARITY_NONE,
#     "&Even parity": PARITY_EVEN,
#     "&Odd parity": PARITY_ODD,
#     "&Mark parity": PARITY_MARK,
#     "&Space parity": PARITY_SPACE
# }
PARITIES = dict(filter(
    lambda p: p[1] in Serial.PARITIES,
    {
        "&No parity": PARITY_NONE,
        "&Even parity": PARITY_EVEN,
        "&Odd parity": PARITY_ODD,
        "&Mark parity": PARITY_MARK,
        "&Space parity": PARITY_SPACE
    }.items()
))
logger.debug(f"Parities available: {PARITIES}")

DEFAULT_PARITY = PARITY_NONE
logger.debug(f"Default parity: {DEFAULT_PARITY}")

STOP_BITS = dict(filter(
    lambda b: b[1] in Serial.STOPBITS,
    {
        "&1 stop bit": STOPBITS_ONE,
        "1.&5 stop bits": STOPBITS_ONE_POINT_FIVE,
        "&2 stop bits": STOPBITS_TWO
    }.items()
))
logger.debug(f"Stop bits available: {STOP_BITS}")

DEFAULT_STOP_BIT = STOPBITS_ONE
logger.debug(f"Default stop bit: {DEFAULT_STOP_BIT}")

NO_FLOW_CONTROL = 0
XON_XOFF_SOFT_FLOW_CONTROL = 1
RTS_CTS_HARD_FLOW_CONTROL = 2
DSR_DTR_HARD_FLOW_CONTROL = 3

FLOW_CONTROLS = {
    "&No flow control": NO_FLOW_CONTROL,
    "&XON/XOFF (software) flow control": XON_XOFF_SOFT_FLOW_CONTROL,
    "&RTS/CTS (hardware) flow control": RTS_CTS_HARD_FLOW_CONTROL,
    "&DSR/DTR (hardware) flow control": DSR_DTR_HARD_FLOW_CONTROL
}
logger.debug(f"Flow control methods available: {FLOW_CONTROLS}")

DEFAULT_FLOW_CONTROL = NO_FLOW_CONTROL
logger.debug(f"Default flow control: {DEFAULT_FLOW_CONTROL}")

NEWLINE_LF = 0
NEWLINE_CR = 1
NEWLINE_CRLF = 2

LINE_ENDINGS = {
    "&Line feed (\\n)": NEWLINE_LF,
    "&Carriage return (\\r)": NEWLINE_CR,
    "Carriage return &and line feed (\\r\\n)": NEWLINE_CRLF
}
logger.debug(f"Line endings available: {LINE_ENDINGS}")

DEFAULT_LINE_ENDING = NEWLINE_LF
# Possible values of platform.system():
#   - Linux
#   - Darwin
#   - Java
#   - Windows
if system() == "Windows":
    DEFAULT_LINE_ENDING = NEWLINE_CRLF

logger.debug(f"Default line ending: {DEFAULT_LINE_ENDING}")
