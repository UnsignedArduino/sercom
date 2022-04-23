from platform import system

from serial import *

COMMON_BAUD_RATES = (
    50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200,
    38400, 57600, 115200
)

HIGH_SPEED_BAUD_RATES = (
    230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000,
    2500000, 3000000, 3500000, 4000000
)

ALL_BAUD_RATES = COMMON_BAUD_RATES + HIGH_SPEED_BAUD_RATES

DEFAULT_BAUD_RATE = 9600

BYTE_SIZES = {
    "&5 bits": FIVEBITS,
    "&6 bits": SIXBITS,
    "&7 bits": SEVENBITS,
    "&8 bits": EIGHTBITS
}

DEFAULT_BYTE_SIZE = EIGHTBITS

PARITIES = {
    "&No parity": PARITY_NONE,
    "&Even parity": PARITY_EVEN,
    "&Odd parity": PARITY_ODD,
    "&Mark parity": PARITY_MARK,
    "&Space parity": PARITY_SPACE
}

DEFAULT_PARITY = PARITY_NONE

STOP_BITS = {
    "&1 stop bit": STOPBITS_ONE,
    "1.&5 stop bits": STOPBITS_ONE_POINT_FIVE,
    "&2 stop bits": STOPBITS_TWO
}

DEFAULT_STOP_BIT = STOPBITS_ONE

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

DEFAULT_FLOW_CONTROL = NO_FLOW_CONTROL

NEWLINE_LF = 0
NEWLINE_CR = 1
NEWLINE_CRLF = 2

LINE_ENDINGS = {
    "&Line feed (\\n)": NEWLINE_LF,
    "&Carriage return (\\r)": NEWLINE_CR,
    "Carriage return &and line feed (\\r\\n)": NEWLINE_CRLF
}

DEFAULT_LINE_ENDING = NEWLINE_LF
# Possible values of platform.system():
#   - Linux
#   - Darwin
#   - Java
#   - Windows
if system() == "Windows":
    DEFAULT_LINE_ENDING = NEWLINE_CRLF
