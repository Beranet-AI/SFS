from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("devices", "0002_alter_device_name_alter_sensor_hardware_address_and_more"),
        ("livestock", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("lactation_stage", models.CharField(blank=True, help_text="Early, mid, late, or dry", max_length=50, null=True)),
                ("parity", models.PositiveIntegerField(default=0, help_text="Number of calvings")),
                ("days_in_milk", models.PositiveIntegerField(blank=True, help_text="Days since last calving", null=True)),
                ("last_calving_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "animal",
                    models.OneToOneField(
                        help_text="Animal record for this cow",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cow_profile",
                        to="livestock.animal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cow",
                "verbose_name_plural": "Cows",
                "db_table": "cows",
            },
        ),
        migrations.CreateModel(
            name="Disease",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("symptoms", models.JSONField(blank=True, help_text="List of dominant symptoms or markers", null=True)),
                (
                    "detection_methods",
                    models.JSONField(blank=True, help_text="Algorithms, heuristics, or lab methods used", null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Disease",
                "verbose_name_plural": "Diseases",
                "ordering": ["name"],
                "db_table": "diseases",
            },
        ),
        migrations.CreateModel(
            name="MLModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("version", models.CharField(default="1.0.0", max_length=50)),
                ("framework", models.CharField(help_text="sklearn, pytorch, tensorflow, onnx, etc.", max_length=50)),
                ("artifact_path", models.CharField(help_text="URI to the serialized model artifact", max_length=500)),
                ("input_schema", models.JSONField(help_text="List of expected features and shapes")),
                ("metrics", models.JSONField(blank=True, help_text="Evaluation metrics for the specific version", null=True)),
                ("is_active", models.BooleanField(default=True, help_text="Flag to indicate preferred version for inference")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "disease",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="models", to="health.disease"),
                ),
            ],
            options={
                "verbose_name": "ML Model",
                "verbose_name_plural": "ML Models",
                "ordering": ["name", "version"],
                "db_table": "ml_models",
                "unique_together": {("name", "version")},
            },
        ),
        migrations.CreateModel(
            name="SensorData",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ts", models.DateTimeField(db_index=True)),
                ("value", models.FloatField()),
                ("unit", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "quality",
                    models.CharField(
                        choices=[("good", "Good"), ("suspect", "Suspect"), ("bad", "Bad")],
                        default="good",
                        max_length=10,
                    ),
                ),
                ("raw_payload", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "cow",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sensor_data",
                        to="health.cow",
                    ),
                ),
                (
                    "sensor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="health_data",
                        to="devices.sensor",
                    ),
                ),
                (
                    "sensor_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="health_sensor_data",
                        to="devices.sensortype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sensor Data",
                "verbose_name_plural": "Sensor Data",
                "ordering": ["-ts"],
                "db_table": "sensor_data",
            },
        ),
        migrations.CreateModel(
            name="Prediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("healthy", "Healthy"), ("suspected", "Suspected"), ("at_risk", "At Risk")],
                        default="healthy",
                        max_length=20,
                    ),
                ),
                (
                    "probability",
                    models.DecimalField(blank=True, decimal_places=4, help_text="Probability or confidence score", max_digits=5, null=True),
                ),
                ("predicted_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("features", models.JSONField(help_text="Feature vector used for prediction")),
                ("feature_window_start", models.DateTimeField(blank=True, null=True)),
                ("feature_window_end", models.DateTimeField(blank=True, null=True)),
                (
                    "cow",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="predictions", to="health.cow"),
                ),
                (
                    "disease",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="predictions", to="health.disease"),
                ),
                (
                    "model",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="predictions", to="health.mlmodel"),
                ),
            ],
            options={
                "verbose_name": "Prediction",
                "verbose_name_plural": "Predictions",
                "ordering": ["-predicted_at"],
                "db_table": "predictions",
            },
        ),
        migrations.CreateModel(
            name="DiseaseRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("suspected", "Suspected"), ("confirmed", "Confirmed"), ("recovered", "Recovered")],
                        default="suspected",
                        max_length=20,
                    ),
                ),
                ("diagnosed_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "cow",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="disease_records", to="health.cow"),
                ),
                (
                    "disease",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="records", to="health.disease"),
                ),
                (
                    "source_prediction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="disease_records",
                        to="health.prediction",
                    ),
                ),
            ],
            options={
                "verbose_name": "Disease Record",
                "verbose_name_plural": "Disease Records",
                "db_table": "disease_records",
            },
        ),
        migrations.AddIndex(
            model_name="cow",
            index=models.Index(fields=["parity", "lactation_stage"], name="cows_parity_a3d715_idx"),
        ),
        migrations.AddIndex(
            model_name="sensordata",
            index=models.Index(fields=["sensor", "ts"], name="sensor_dat_sensor__ef4085_idx"),
        ),
        migrations.AddIndex(
            model_name="sensordata",
            index=models.Index(fields=["cow", "ts"], name="sensor_dat_cow_id_43b0ce_idx"),
        ),
        migrations.AddIndex(
            model_name="prediction",
            index=models.Index(fields=["cow", "predicted_at"], name="predictio_cow_id_12713d_idx"),
        ),
        migrations.AddIndex(
            model_name="prediction",
            index=models.Index(fields=["disease", "predicted_at"], name="predictio_disease__e98bfc_idx"),
        ),
        migrations.AddIndex(
            model_name="diseaserecord",
            index=models.Index(fields=["cow", "disease", "diagnosed_at"], name="disease_r_cow_id_3169c3_idx"),
        ),
    ]
