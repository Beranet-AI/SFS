from enum import Enum

class DeviceType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    AMMONIA = "ammonia"
    HEART_RATE = "heart_rate"
    MOTION = "motion"
