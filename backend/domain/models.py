"""Backward-compatible alias for domain entities.

The canonical home for domain objects is :mod:`backend.domain.entities`.
This module re-exports the same dataclasses so existing imports do not
break while the codebase migrates toward a stricter domain/application
separation.
"""

from .entities import (
    Alert,
    AlertRule,
    Animal,
    Barn,
    Device,
    Farm,
    RfidTag,
    Sensor,
    SensorReading,
    SensorType,
    Zone,
)

__all__ = [
    "Alert",
    "AlertRule",
    "Animal",
    "Barn",
    "Device",
    "Farm",
    "RfidTag",
    "Sensor",
    "SensorReading",
    "SensorType",
    "Zone",
]
