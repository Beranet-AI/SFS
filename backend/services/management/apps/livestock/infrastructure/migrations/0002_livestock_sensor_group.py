from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("livestock", "0001_initial"),
        ("devices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LivestockSensorGroupModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "livestock",
                    models.OneToOneField(
                        on_delete=models.deletion.CASCADE,
                        related_name="sensor_group",
                        to="livestock.livestockmodel",
                    ),
                ),
                (
                    "rfid_device",
                    models.OneToOneField(
                        on_delete=models.deletion.PROTECT,
                        related_name="rfid_livestock_group",
                        to="devices.devicemodel",
                    ),
                ),
                (
                    "sensors",
                    models.ManyToManyField(
                        blank=True,
                        related_name="livestock_sensor_groups",
                        to="devices.devicemodel",
                    ),
                ),
            ],
        ),
    ]
