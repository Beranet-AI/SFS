from enum import Enum

class DeviceRole(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    GATEWAY = "gateway"
