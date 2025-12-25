from enum import Enum

class DeviceType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    AMMONIA = "ammonia"
    HEART_RATE = "heart_rate"
    MOTION = "motion"
    OZONE = "ozone"
    FAN = "fan"
    VENT = "vent"
    VALVE = "valve"
    HEATER = "heater"
    COOLER = "cooler"
