"""Simple rules engine for evaluating sensor readings."""

from __future__ import annotations

import logging
import operator
from typing import Any, Dict, Iterable, List, Mapping


logger = logging.getLogger(__name__)

COMPARATORS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


def evaluate_rules_for_reading(
    rules: Iterable[Mapping[str, Any]],
    reading: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """Return rules that are triggered for the supplied reading."""

    sensor_id = reading.get("sensor_id") or reading.get("sensor")
    value = reading.get("value")

    if sensor_id is None or value is None:
        return []

    triggered: List[Dict[str, Any]] = []
    for rule in rules:
        params = rule.get("params") or {}
        rule_sensor_id = params.get("sensor_id")
        threshold = params.get("threshold")
        operator_symbol = params.get("operator", ">")

        if rule_sensor_id is not None and rule_sensor_id != sensor_id:
            continue
        if threshold is None:
            continue

        if _compare(value, threshold, operator_symbol):
            triggered.append(dict(rule))

    return triggered


def _compare(value: Any, threshold: Any, operator_symbol: str) -> bool:
    comparator = COMPARATORS.get(operator_symbol)
    if comparator is None:
        logger.warning("Unknown operator '%s' provided to rules engine", operator_symbol)
        return False

    try:
        return comparator(float(value), float(threshold))
    except (TypeError, ValueError):
        logger.warning(
            "Comparison failed for value=%r threshold=%r operator=%s", value, threshold, operator_symbol
        )
        return False
