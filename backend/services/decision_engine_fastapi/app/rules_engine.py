# decision_engine_fastapi/app/rules_engine.py

from typing import List, Dict, Any


def evaluate_rules_for_reading(
    rules: List[Dict[str, Any]],
    reading: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    rules: لیست قوانین فعال بر اساس خروجی API Django از /alert-rules/
    reading: داده SensorReading که همین الان ثبت شده/یا می‌خواهیم ثبت کنیم.
    خروجی: لیست قوانین تریگر شده
    """

    triggered: List[Dict[str, Any]] = []

    sensor_id = reading.get("sensor_id") or reading.get("sensor")
    value = reading.get("value")

    if sensor_id is None or value is None:
        return triggered

    for rule in rules:
        params = rule.get("params") or {}
        rule_sensor_id = params.get("sensor_id")
        threshold = params.get("threshold")
        operator = params.get("operator", ">")

        # اگر rule برای سنسور خاصی تعریف شده و با این سنسور نمی‌خواند → رد
        if rule_sensor_id is not None and rule_sensor_id != sensor_id:
            continue

        if threshold is None:
            continue

        if _compare(value, threshold, operator):
            triggered.append(rule)

    return triggered


def _compare(value: float, threshold: float, operator: str) -> bool:
    if operator == ">":
        return value > threshold
    if operator == ">=":
        return value >= threshold
    if operator == "<":
        return value < threshold
    if operator == "<=":
        return value <= threshold
    if operator == "==":
        return value == threshold
    if operator == "!=":
        return value != threshold
    # اگر operator ناشناخته بود، فعلاً false
    return False
