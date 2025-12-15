from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("health", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cow",
            name="breed",
            field=models.CharField(blank=True, help_text="Breed identifier or code", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cow",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="prediction",
            name="lead_time_hours",
            field=models.FloatField(
                blank=True, help_text="Lead time between prediction and diagnosis window start", null=True
            ),
        ),
        migrations.AddField(
            model_name="sensordata",
            name="aggregation",
            field=models.CharField(blank=True, help_text="raw, minute, hourly, daily", max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="sensordata",
            name="sample_interval_seconds",
            field=models.PositiveIntegerField(
                blank=True, help_text="Sampling interval used to compute the observation", null=True
            ),
        ),
        migrations.CreateModel(
            name="ClinicalEvent",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("diagnosis", "Diagnosis"),
                            ("observation", "Observation"),
                            ("treatment", "Treatment"),
                            ("lab", "Lab"),
                        ],
                        max_length=20,
                    ),
                ),
                ("occurred_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "symptom",
                    models.CharField(blank=True, help_text="Primary symptom or observation", max_length=200, null=True),
                ),
                ("severity", models.CharField(blank=True, max_length=50, null=True)),
                ("source", models.CharField(default="manual", help_text="manual, vet, app, ingest", max_length=50)),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="clinical_events", to="health.cow"
                    ),
                ),
                (
                    "disease",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="clinical_events",
                        to="health.disease",
                    ),
                ),
            ],
            options={
                "verbose_name": "Clinical Event",
                "verbose_name_plural": "Clinical Events",
                "db_table": "clinical_events",
            },
        ),
        migrations.CreateModel(
            name="LabResult",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("parameter", models.CharField(max_length=100)),
                ("value", models.FloatField()),
                ("unit", models.CharField(blank=True, max_length=20, null=True)),
                ("result_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("reference_range", models.CharField(blank=True, max_length=100, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "clinical_event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lab_results",
                        to="health.clinicalevent",
                    ),
                ),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="lab_results", to="health.cow"
                    ),
                ),
                (
                    "disease",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lab_results",
                        to="health.disease",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lab Result",
                "verbose_name_plural": "Lab Results",
                "db_table": "lab_results",
            },
        ),
        migrations.CreateModel(
            name="ManagementEvent",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("pen_move", "Pen Move"),
                            ("diet_change", "Diet Change"),
                            ("milking_schedule", "Milking Schedule"),
                            ("seasonal", "Seasonal"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("occurred_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("metadata", models.JSONField(blank=True, null=True)),
                (
                    "cow",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="management_events",
                        to="health.cow",
                    ),
                ),
            ],
            options={
                "verbose_name": "Management Event",
                "verbose_name_plural": "Management Events",
                "db_table": "management_events",
            },
        ),
        migrations.CreateModel(
            name="TreatmentLog",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("treatment_type", models.CharField(max_length=200)),
                ("medication", models.CharField(blank=True, max_length=200, null=True)),
                ("dose", models.CharField(blank=True, max_length=100, null=True)),
                ("administered_by", models.CharField(blank=True, max_length=100, null=True)),
                ("started_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "clinical_event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="treatments",
                        to="health.clinicalevent",
                    ),
                ),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="treatments", to="health.cow"
                    ),
                ),
                (
                    "disease",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="treatments",
                        to="health.disease",
                    ),
                ),
            ],
            options={
                "verbose_name": "Treatment Log",
                "verbose_name_plural": "Treatment Logs",
                "db_table": "treatment_logs",
            },
        ),
        migrations.AddIndex(
            model_name="clinicalevent",
            index=models.Index(fields=["cow", "occurred_at"], name="clinical_e_cow_id_53937e_idx"),
        ),
        migrations.AddIndex(
            model_name="clinicalevent",
            index=models.Index(fields=["disease", "event_type"], name="clinical_e_disease__931efb_idx"),
        ),
        migrations.AddIndex(
            model_name="labresult",
            index=models.Index(fields=["cow", "result_at"], name="lab_result_cow_id_445952_idx"),
        ),
        migrations.AddIndex(
            model_name="labresult",
            index=models.Index(fields=["disease", "parameter"], name="lab_result_disease__b83356_idx"),
        ),
        migrations.AddIndex(
            model_name="managementevent",
            index=models.Index(fields=["event_type", "occurred_at"], name="management_event_type__6b2f35_idx"),
        ),
        migrations.AddIndex(
            model_name="treatmentlog",
            index=models.Index(fields=["cow", "started_at"], name="treatment_cow_id_94521c_idx"),
        ),
        migrations.AddIndex(
            model_name="treatmentlog",
            index=models.Index(fields=["disease", "treatment_type"], name="treatment_disease_5bad31_idx"),
        ),
    ]
