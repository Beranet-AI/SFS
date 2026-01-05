from enum import Enum


class CommandCategory(str, Enum):
    QUERY = "Query"
    CONFIGURATION = "Configuration"
    CONTROL = "Control"
