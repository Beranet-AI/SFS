from __future__ import annotations
from typing import Callable, Dict
from django.db import transaction
from alerts.models import AlertLog, AlertRule
from telemetry.models import SensorReading

_OPERATOR_FN: Dict[str, Callable[[float, float], bool]] = {
    ">": lambda v, t: v > t,
    "<": lambda v, t: v < t,
    ">=": lambda v, t: v >= t,
    "<=": lambda v, t: v <= t,
    "==": lambda v, t: v == t,
    "!=": lambda v, t: v != t,
}


def evaluate_alerts_for_reading(reading: SensorReading) -> None:
    """Evaluate alert rules for the given reading and log triggered alerts."""

    rules = AlertRule.objects.select_related("sensor").filter(sensor=reading.sensor, enabled=True)
    if not rules.exists():
        return

    triggered: list[AlertLog] = []
    for rule in rules:
        comparator = _OPERATOR_FN.get(rule.operator)
        if comparator is None:
            continue
        if comparator(reading.value, rule.threshold_value):
            triggered.append(
                AlertLog(
                    sensor=reading.sensor,
                    value=reading.value,
                    triggered_at=reading.ts,
                    alert_rule=rule,
                )
            )

    if triggered:
        # Batch insert for efficiency and atomicity
        with transaction.atomic():
            AlertLog.objects.bulk_create(triggered)
