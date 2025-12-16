from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IncidentModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("severity", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=16)),
                ("title", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("metric", models.CharField(blank=True, max_length=64, null=True)),
                ("value", models.FloatField(blank=True, null=True)),
                ("farm_id", models.UUIDField()),
                ("barn_id", models.UUIDField(blank=True, null=True)),
                ("zone_id", models.UUIDField(blank=True, null=True)),
                ("device_id", models.UUIDField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "incidents",
                "ordering": ["-created_at"],
            },
        ),
    ]
