# Generated manually because Django is unavailable in the container.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0001_initial"),
        ("devices", "0002_alter_device_name_alter_sensor_hardware_address_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alertrule",
            name="scope",
        ),
        migrations.AddField(
            model_name="alertrule",
            name="sensor",
            field=models.ForeignKey(
                blank=True,
                help_text="قانون برای یک سنسور مشخص",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="alert_rules",
                to="devices.sensor",
            ),
        ),
        migrations.AddField(
            model_name="alertrule",
            name="sensor_type",
            field=models.ForeignKey(
                blank=True,
                help_text="یا بر اساس نوع سنسور اعمال شود",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="alert_rules",
                to="devices.sensortype",
            ),
        ),
        migrations.AddField(
            model_name="alertrule",
            name="threshold_value",
            field=models.FloatField(default=0.0, help_text="آستانهٔ هشدار"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="alertrule",
            name="operator",
            field=models.CharField(
                choices=[("greater_than", "Greater than"), ("less_than", "Less than")],
                default="greater_than",
                help_text="اپراتور مقایسه با آستانه",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="alertrule",
            name="condition_expression",
            field=models.CharField(
                blank=True,
                help_text="عبارت شرطی اختیاری برای قوانین پیشرفته",
                max_length=500,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="alert",
            name="reading_value",
            field=models.FloatField(
                blank=True,
                help_text="مقدار خوانده‌شده که قانون را نقض کرده است",
                null=True,
            ),
        ),
        migrations.AddIndex(
            model_name="alert",
            index=models.Index(fields=["status", "raised_at"], name="alerts_status_raised_idx"),
        ),
    ]
