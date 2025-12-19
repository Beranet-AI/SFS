from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TelemetryModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("device_id", models.CharField(max_length=64)),
                ("livestock_id", models.CharField(max_length=64)),
                ("metric", models.CharField(max_length=64)),
                ("value", models.FloatField()),
                ("recorded_at", models.DateTimeField()),
            ],
        ),
        migrations.AddIndex(
            model_name="telemetrymodel",
            index=models.Index(fields=["livestock_id", "recorded_at"], name="tele_livestock_time_idx"),
        ),
        migrations.AddIndex(
            model_name="telemetrymodel",
            index=models.Index(fields=["device_id", "recorded_at"], name="tele_device_time_idx"),
        ),
    ]
