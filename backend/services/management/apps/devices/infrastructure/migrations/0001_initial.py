from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeviceModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("serial", models.CharField(max_length=128, unique=True)),
                ("device_type", models.CharField(max_length=64)),
                ("status", models.CharField(max_length=32)),
                ("assigned_livestock_id", models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
    ]
