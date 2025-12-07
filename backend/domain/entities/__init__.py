"""Domain entities for the SmartFarm system.

These dataclasses capture the core aggregate roots and value objects that
are shared between services. They intentionally avoid framework-specific
concerns to keep the domain portable across microservices.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional, Dict


@dataclass
class Farm:
    id: int
    name: str
    location: str
    barns: List["Barn"]


@dataclass
class Barn:
    id: int
    farm: Farm
    name: str
    description: Optional[str]
    zones: List["Zone"]


@dataclass
class Zone:
    id: int
    barn: Barn
    name: str
    description: Optional[str]


@dataclass
class Device:
    id: int
    farm: Farm
    barn: Optional[Barn]
    zone: Optional[Zone]
    type: str  # edge_controller, sensor_node, camera, ...
    serial_number: Optional[str]
    status: str  # online/offline/fault
    last_seen_at: Optional[datetime]


@dataclass
class SensorType:
    id: int
    code: str  # temperature, humidity, ammonia, rfid, camera
    unit: str  # °C, %, ppm, ...
    min_value: Optional[float]
    max_value: Optional[float]


@dataclass
class Sensor:
    id: int
    device: Device
    sensor_type: SensorType
    name: str
    hardware_address: Optional[str]  # channel/port/Modbus address
    is_active: bool


@dataclass
class SensorReading:
    id: int
    sensor: Sensor
    ts: datetime
    value: float
    raw_payload: Optional[Dict]
    quality: str  # good/bad/suspect


@dataclass
class Animal:
    id: int
    farm: Farm
    barn: Optional[Barn]
    current_zone: Optional[Zone]
    rfid_tag: Optional["RfidTag"]
    species: str
    breed: Optional[str]
    birth_date: Optional[date]
    status: str  # alive/sold/dead


@dataclass
class RfidTag:
    id: int
    farm: Farm
    tag_code: str
    status: str  # free/assigned/lost
    assigned_animal: Optional[Animal]


@dataclass
class AlertRule:
    id: int
    name: str
    scope: str  # sensor/barn/farm
    severity: str  # info/warn/critical
    condition_expression: str  # expression consumed by rule engine
    is_active: bool


@dataclass
class Alert:
    id: int
    rule: Optional[AlertRule]
    farm: Farm
    barn: Optional[Barn]
    sensor: Optional[Sensor]
    raised_at: datetime
    resolved_at: Optional[datetime]
    severity: str  # info/warn/critical
    message: str
    status: str  # open/ack/resolved
