from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IncidentModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("livestock_id", models.CharField(max_length=64)),
                ("severity", models.CharField(max_length=32)),
                ("status", models.CharField(max_length=32)),
                ("source", models.CharField(max_length=32)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField()),
                ("acknowledged_at", models.DateTimeField(null=True, blank=True)),
                ("resolved_at", models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
