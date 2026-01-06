from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("commands", "0001_discovery_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="NetworkScanResultModel",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("scan_id", models.UUIDField(db_index=True)),
                ("device_uid", models.CharField(max_length=128)),
                ("device_name", models.CharField(blank=True, max_length=255, null=True)),
                ("device_category", models.CharField(max_length=64)),
                ("device_type", models.CharField(max_length=64)),
                ("protocol", models.CharField(blank=True, default="", max_length=64)),
                ("adapter_type", models.CharField(blank=True, default="", max_length=64)),
                ("direction", models.CharField(choices=[("uplink_only", "Uplink Only"), ("bidirectional", "Bidirectional")], max_length=32)),
                ("supports_commands", models.BooleanField(default=False)),
                ("supported_command_categories", models.JSONField(blank=True, default=list)),
                ("ip_address", models.CharField(blank=True, max_length=64, null=True)),
                ("port", models.IntegerField(blank=True, null=True)),
                ("network_address", models.CharField(blank=True, max_length=128, null=True)),
                ("signal_strength", models.FloatField(blank=True, null=True)),
                ("firmware_version", models.CharField(blank=True, max_length=128, null=True)),
                ("vendor", models.CharField(blank=True, max_length=128, null=True)),
                ("model", models.CharField(blank=True, max_length=128, null=True)),
                ("battery_level", models.FloatField(blank=True, null=True)),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                ("discovered_at", models.DateTimeField(blank=True, null=True)),
                ("scan_status", models.CharField(choices=[("new", "New"), ("known", "Known"), ("changed", "Changed")], default="new", max_length=16)),
                ("raw_capabilities", models.JSONField(blank=True, null=True)),
                ("is_registered", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Discover",
                "verbose_name_plural": "Discover",
                "db_table": "commands_network_scan_result",
                "ordering": ["-discovered_at", "-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="networkscanresultmodel",
            index=models.Index(fields=["scan_id", "device_uid"], name="commands_ne_scan_id_4e8e4b_idx"),
        ),
        migrations.AddIndex(
            model_name="networkscanresultmodel",
            index=models.Index(fields=["scan_status"], name="commands_ne_scan_st_01e0ff_idx"),
        ),
        migrations.AddIndex(
            model_name="networkscanresultmodel",
            index=models.Index(fields=["is_registered"], name="commands_ne_is_regi_7fc269_idx"),
        ),
        migrations.AddConstraint(
            model_name="networkscanresultmodel",
            constraint=models.UniqueConstraint(fields=("scan_id", "device_uid"), name="uniq_network_scan_device"),
        ),
    ]
