from datetime import datetime, timezone

from django.test import TestCase

from alerts.models import AlertLog, AlertRule
from management.application.alerts.service import evaluate_alerts_for_reading
from devices.models import Device, Sensor, SensorType
from farm.models import Farm
from telemetry.models import SensorReading


class AlertEvaluationTests(TestCase):
    def setUp(self):
        self.farm = Farm.objects.create(name="Farm A")
        self.device = Device.objects.create(farm=self.farm, type="sensor_node", name="node-1")
        self.sensor_type = SensorType.objects.create(code="temperature", name="Temperature", unit="C")
        self.sensor = Sensor.objects.create(device=self.device, sensor_type=self.sensor_type, name="temp-1")
        self.rule = AlertRule.objects.create(sensor=self.sensor, threshold_value=10.0, operator=">")

    def test_log_created_when_threshold_crossed(self):
        reading = SensorReading.objects.create(
            sensor=self.sensor,
            ts=datetime.now(timezone.utc),
            value=12.5,
        )

        evaluate_alerts_for_reading(reading)

        self.assertEqual(AlertLog.objects.count(), 1)
        log = AlertLog.objects.first()
        self.assertEqual(log.alert_rule, self.rule)
        self.assertAlmostEqual(log.value, 12.5)

    def test_no_log_when_disabled(self):
        self.rule.enabled = False
        self.rule.save()

        reading = SensorReading.objects.create(
            sensor=self.sensor,
            ts=datetime.now(timezone.utc),
            value=15.0,
        )

        evaluate_alerts_for_reading(reading)

        self.assertEqual(AlertLog.objects.count(), 0)
