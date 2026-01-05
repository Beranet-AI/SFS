from enum import Enum


class CommandType(str, Enum):
    GET_CONNECTED_DEVICES = "get_connected_devices"
    SET_NETWORK = "set_network"
    SET_PROTOCOL = "set_protocol"
    DISCOVER = "DISCOVER"
    ON_OFF = "ON_OFF"
    REBOOT = "REBOOT"
