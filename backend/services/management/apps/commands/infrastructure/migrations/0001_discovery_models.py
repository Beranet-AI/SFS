import uuid

from django.utils import timezone

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("devices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscoverySessionModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True
                    ),
                ),
                ("edge_node_id", models.CharField(max_length=64)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=16,
                    ),
                ),
                ("started_by", models.CharField(blank=True, default="", max_length=64)),
                ("started_at", models.DateTimeField(default=timezone.now)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("device_count", models.IntegerField(default=0)),
                ("error_message", models.TextField(blank=True, default="")),
            ],
            options={
                "db_table": "commands_discovery_session",
                "ordering": ["-started_at"],
                "verbose_name": "Discover Devices",
                "verbose_name_plural": "Discover Devices",
            },
        ),
        migrations.CreateModel(
            name="DiscoveredDeviceModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True
                    ),
                ),
                ("device_id", models.CharField(max_length=128)),
                (
                    "device_type",
                    models.CharField(blank=True, default="", max_length=128),
                ),
                ("ip_address", models.CharField(blank=True, default="", max_length=64)),
                ("capabilities", models.JSONField(blank=True, default=dict)),
                ("raw_payload", models.JSONField(blank=True, default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("registered", "Registered")],
                        default="new",
                        max_length=16,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "registered_device",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="discovery_records",
                        to="devices.devicemodel",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="devices",
                        to="commands.discoverysessionmodel",
                    ),
                ),
            ],
            options={
                "db_table": "commands_discovered_device",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="discoverysessionmodel",
            index=models.Index(
                fields=["edge_node_id", "started_at"],
                name="commands_dis_edge_no_2b3579_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="discoverysessionmodel",
            index=models.Index(
                fields=["status"], name="commands_dis_status_8095ed_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="discovereddevicemodel",
            index=models.Index(
                fields=["session", "device_id"],
                name="commands_dis_session_0c2452_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="discovereddevicemodel",
            index=models.Index(
                fields=["status"], name="commands_dis_status_1c4744_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="discovereddevicemodel",
            constraint=models.UniqueConstraint(
                fields=("session", "device_id"),
                name="uniq_discovery_session_device",
            ),
        ),
        migrations.AddField(
            model_name="discoverysessionmodel",
            name="command",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="discovery_sessions",
                to="commands.commandmodel",
            ),
        ),
    ]
