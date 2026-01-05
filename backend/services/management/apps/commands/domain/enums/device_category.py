from enum import Enum


class DeviceCategory(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    DEVICE = "Device"
    LIVESTOCK = "Livestock"
    LOCATION = "Location"
