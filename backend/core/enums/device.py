from enum import Enum


class DeviceKind(str, Enum):
    SENSOR = "sensor"
    CAMERA = "camera"
    RFID = "rfid"
    MOTION_SENSOR = "motion_sensor"
    GATEWAY = "gateway"
    OTHER = "other"


class SensorMetric(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    AMMONIA = "ammonia"
    HEART_RATE = "heart_rate"
    MOVEMENT_SCORE = "movement_score"
    WEIGHT = "weight"
    MILK_YIELD = "milk_yield"
