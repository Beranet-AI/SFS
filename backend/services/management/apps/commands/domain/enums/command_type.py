from enum import Enum


class CommandType(str, Enum):
    DISCOVER = "DISCOVER"
    ON_OFF = "ON_OFF"
    REBOOT = "REBOOT"
