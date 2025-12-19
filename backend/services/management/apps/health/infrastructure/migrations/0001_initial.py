from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MedicalRecordModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("livestock_id", models.CharField(max_length=64)),
                ("diagnosis", models.CharField(max_length=64)),
                ("notes", models.TextField()),
                ("recorded_at", models.DateTimeField()),
            ],
        ),
    ]
