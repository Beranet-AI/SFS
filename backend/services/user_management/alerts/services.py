from __future__ import annotations

from typing import Iterable

from django.db import models

from devices.models import Sensor
from telemetry.models import SensorReading

from .models import Alert, AlertRule


def _rule_matches_value(rule: AlertRule, value: float) -> bool:
    if rule.operator == "greater_than":
        return value > rule.threshold_value
    if rule.operator == "less_than":
        return value < rule.threshold_value
    return False


def evaluate_alerts_for_reading(reading: SensorReading) -> Iterable[Alert]:
    """
    بررسی قوانین فعال و ثبت هشدار در صورت نقض آستانه.
    هر بار که SensorReading ذخیره می‌شود، این تابع صدا زده می‌شود.
    """

    sensor: Sensor = reading.sensor
    sensor_type = sensor.sensor_type
    device = sensor.device

    rules = AlertRule.objects.filter(is_active=True).filter(
        models.Q(sensor=sensor) | models.Q(sensor_type=sensor_type)
    )

    triggered: list[Alert] = []

    for rule in rules:
        if not _rule_matches_value(rule, reading.value):
            continue

        message = (
            f"سنسور {sensor.name} مقدار {reading.value:.2f}{sensor_type.unit} "
            f"را ثبت کرد که شرط {rule.name} ({rule.operator} {rule.threshold_value}) را نقض می‌کند."
        )

        alert = Alert.objects.create(
            rule=rule,
            farm=device.farm,
            barn=device.barn,
            zone=device.zone,
            sensor=sensor,
            severity=rule.severity,
            reading_value=reading.value,
            message=message,
            status="open",
            raised_at=reading.ts,
            extra_data={
                "sensor_type": sensor_type.code,
                "sensor_type_name": sensor_type.name,
            },
        )
        triggered.append(alert)

    return triggered
