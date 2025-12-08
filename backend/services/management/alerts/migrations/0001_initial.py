from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("devices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlertRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("threshold_value", models.FloatField()),
                (
                    "operator",
                    models.CharField(
                        choices=[(">", ">"), ("<", "<"), (">=", ">="), ("<=", "<="), ("==", "=="), ("!=", "!=")],
                        max_length=2,
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "sensor",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alert_rules", to="devices.sensor"),
                ),
            ],
            options={
                "db_table": "alert_rules",
                "indexes": [
                    models.Index(fields=["sensor", "enabled"], name="alert_rules_sensor_id_enabled_0ae7d5_idx"),
                ],
                "verbose_name": "Alert Rule",
                "verbose_name_plural": "Alert Rules",
            },
        ),
        migrations.CreateModel(
            name="AlertLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.FloatField()),
                ("triggered_at", models.DateTimeField()),
                (
                    "alert_rule",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="logs", to="alerts.alertrule"),
                ),
                (
                    "sensor",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="alert_logs", to="devices.sensor"),
                ),
            ],
            options={
                "db_table": "alert_logs",
                "ordering": ["-triggered_at"],
                "verbose_name": "Alert Log",
                "verbose_name_plural": "Alert Logs",
                "indexes": [
                    models.Index(fields=["sensor", "triggered_at"], name="alert_logs_sensor_id_trigge_b941a9_idx"),
                    models.Index(fields=["alert_rule", "triggered_at"], name="alert_logs_alert_rule__0ce3d0_idx"),
                ],
            },
        ),
    ]
