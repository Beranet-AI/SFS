from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LivestockModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("tag", models.CharField(max_length=64)),
                ("farm_id", models.CharField(max_length=64)),
                ("barn", models.CharField(max_length=64)),
                ("zone", models.CharField(max_length=64)),
                ("health_state", models.CharField(default="healthy", max_length=32)),
                ("health_confidence", models.FloatField(default=1.0)),
                ("health_evaluated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
