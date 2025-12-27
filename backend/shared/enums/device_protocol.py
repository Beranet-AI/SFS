from enum import Enum

class DeviceProtocol(str, Enum):
    HTTP_JSON = "http_json"
    MQTT = "mqtt"
    MODBUS = "modbus"
    OPC_UA = "opc_ua"
    LABVIEW = "labview"
