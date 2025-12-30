from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.farms.models import FarmModel
from apps.livestock.models import LivestockModel
from apps.incidents.models import IncidentModel, IncidentSeverity, IncidentStatus
from apps.telemetry.models import TelemetryModel
from apps.commands.models import CommandModel, CommandStatus, CommandTargetKind


class Command(BaseCommand):
    help = "Seed demo data for management service (farms, livestock, incidents, telemetry, commands)."

    def handle(self, *args, **options):
        now = timezone.now()

        farms = [
            {"name": "Shiraz North Farm"},
            {"name": "Qazvin Greenhouse"},
            {"name": "Tabriz Research Hub"},
        ]

        farm_objs = []
        for farm in farms:
            obj, _ = FarmModel.objects.get_or_create(name=farm["name"])
            farm_objs.append(obj)

        livestock_rows = [
            {
                "tag": "LS-2041",
                "farm_id": str(farm_objs[0].id),
                "barn": "Barn A",
                "zone": "Zone 3",
                "health_state": "healthy",
                "health_confidence": 0.92,
                "health_evaluated_at": now - timedelta(hours=1),
            },
            {
                "tag": "LS-2088",
                "farm_id": str(farm_objs[0].id),
                "barn": "Barn B",
                "zone": "Zone 1",
                "health_state": "at_risk",
                "health_confidence": 0.74,
                "health_evaluated_at": now - timedelta(hours=2),
            },
            {
                "tag": "LS-3120",
                "farm_id": str(farm_objs[1].id),
                "barn": "Barn C",
                "zone": "Zone 2",
                "health_state": "sick",
                "health_confidence": 0.61,
                "health_evaluated_at": now - timedelta(hours=3),
            },
            {
                "tag": "LS-4189",
                "farm_id": str(farm_objs[2].id),
                "barn": "Barn A",
                "zone": "Zone 5",
                "health_state": "critical",
                "health_confidence": 0.48,
                "health_evaluated_at": now - timedelta(hours=6),
            },
        ]

        livestock_objs = []
        for row in livestock_rows:
            obj, _ = LivestockModel.objects.get_or_create(
                tag=row["tag"],
                defaults=row,
            )
            livestock_objs.append(obj)

        incidents = [
            {
                "source": "health-monitor",
                "title": "Abnormal respiration detected",
                "description": "Abnormal respiration detected in Zone 1",
                "severity": IncidentSeverity.HIGH,
                "status": IncidentStatus.ACKNOWLEDGED,
                "livestock_id": livestock_objs[1].tag,
                "occurred_at": now - timedelta(hours=4),
            },
            {
                "source": "iot-gateway",
                "title": "Telemetry loss detected",
                "description": "Telemetry loss detected for 12 minutes",
                "severity": IncidentSeverity.CRITICAL,
                "status": IncidentStatus.OPEN,
                "livestock_id": livestock_objs[2].tag,
                "occurred_at": now - timedelta(hours=2),
            },
            {
                "source": "ai-decision",
                "title": "Temperature normalized",
                "description": "Temperature spike normalized after cooling command",
                "severity": IncidentSeverity.MEDIUM,
                "status": IncidentStatus.RESOLVED,
                "livestock_id": livestock_objs[0].tag,
                "occurred_at": now - timedelta(hours=7),
            },
        ]

        for row in incidents:
            IncidentModel.objects.get_or_create(
                source=row["source"],
                title=row["title"],
                livestock_id=row["livestock_id"],
                defaults=row,
            )

        telemetry_rows = []
        for i in range(12):
            timestamp = now - timedelta(hours=12 - i)
            telemetry_rows.extend(
                [
                    {
                        "device_id": "dev-45",
                        "livestock_id": livestock_objs[0].tag,
                        "metric": "Temperature",
                        "value": 37.5 + (i * 0.03),
                        "recorded_at": timestamp,
                    },
                    {
                        "device_id": "dev-45",
                        "livestock_id": livestock_objs[0].tag,
                        "metric": "Humidity",
                        "value": 54 + (i * 0.2),
                        "recorded_at": timestamp,
                    },
                ]
            )

        for row in telemetry_rows:
            TelemetryModel.objects.get_or_create(
                device_id=row["device_id"],
                livestock_id=row["livestock_id"],
                metric=row["metric"],
                recorded_at=row["recorded_at"],
                defaults=row,
            )

        commands = [
            {
                "command_name": "Adjust Ventilation",
                "target_kind": CommandTargetKind.LOCATION,
                "target_id": str(farm_objs[0].id),
                "status": CommandStatus.SUCCEEDED,
                "source": "automation",
                "created_at": now - timedelta(hours=2),
            },
            {
                "command_name": "Increase Cooling",
                "target_kind": CommandTargetKind.LIVESTOCK,
                "target_id": livestock_objs[2].tag,
                "status": CommandStatus.DISPATCHED,
                "source": "ai",
                "created_at": now - timedelta(minutes=40),
            },
            {
                "command_name": "Schedule Vet Visit",
                "target_kind": CommandTargetKind.LIVESTOCK,
                "target_id": livestock_objs[3].tag,
                "status": CommandStatus.PENDING,
                "source": "care-team",
                "created_at": now - timedelta(minutes=20),
            },
        ]

        for row in commands:
            CommandModel.objects.get_or_create(
                command_name=row["command_name"],
                target_id=row["target_id"],
                created_at=row["created_at"],
                defaults=row,
            )

        self.stdout.write(self.style.SUCCESS("Seeded demo data successfully."))
