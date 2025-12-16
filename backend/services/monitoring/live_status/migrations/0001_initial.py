from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LiveStatusRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="نام قانون وضعیت (مثلاً High Temperature in Barn 1)", max_length=200)),
                ("description", models.TextField(blank=True, help_text="توضیح قانون وضعیت", null=True)),
                ("threshold_value", models.FloatField(help_text="آستانهٔ وضعیت")),
                ("operator", models.CharField(choices=[("greater_than", "Greater than"), ("less_than", "Less than")], default="greater_than", help_text="اپراتور مقایسه با آستانه", max_length=20)),
                ("severity", models.CharField(choices=[("info", "Info"), ("warn", "Warning"), ("critical", "Critical")], default="warn", max_length=20)),
                ("condition_expression", models.CharField(blank=True, help_text="عبارت شرطی اختیاری برای قوانین پیشرفته", max_length=500, null=True)),
                ("params", models.JSONField(blank=True, help_text="پارامترهای قانون (thresholds, window, ...)", null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("farm", models.ForeignKey(help_text="این قانون برای کدام مزرعه است؟", on_delete=django.db.models.deletion.CASCADE, related_name="live_status_rules", to="farm.farm")),
                ("sensor", models.ForeignKey(blank=True, help_text="قانون برای یک سنسور مشخص", null=True, on_delete=django.db.models.deletion.CASCADE, related_name="live_status_rules", to="devices.sensor")),
                ("sensor_type", models.ForeignKey(blank=True, help_text="یا بر اساس نوع سنسور اعمال شود", null=True, on_delete=django.db.models.deletion.CASCADE, related_name="live_status_rules", to="devices.sensortype")),
            ],
            options={
                "db_table": "live_status_rules",
                "ordering": ["farm", "severity", "name"],
                "verbose_name": "Live Status Rule",
                "verbose_name_plural": "Live Status Rules",
            },
        ),
        migrations.CreateModel(
            name="LiveStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("severity", models.CharField(choices=[("info", "Info"), ("warn", "Warning"), ("critical", "Critical")], default="warn", max_length=20)),
                ("reading_value", models.FloatField(blank=True, help_text="مقدار خوانده‌شده که قانون را نقض کرده است", null=True)),
                ("message", models.TextField(help_text="پیام وضعیت برای نمایش به کاربر")),
                ("state", models.CharField(choices=[("active", "Active"), ("cleared", "Cleared")], default="active", max_length=20)),
                ("raised_at", models.DateTimeField(help_text="زمان ایجاد وضعیت")),
                ("cleared_at", models.DateTimeField(blank=True, help_text="زمان برطرف شدن وضعیت (در صورت وجود)", null=True)),
                ("extra_data", models.JSONField(blank=True, help_text="داده‌های کمکی (مقادیر سنسور، context، ...)", null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("animal", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="live_statuses", to="livestock.animal")),
                ("barn", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="live_statuses", to="farm.barn")),
                ("farm", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="live_statuses", to="farm.farm")),
                ("rule", models.ForeignKey(blank=True, help_text="قانونی که این وضعیت را ایجاد کرده (در صورت وجود)", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="live_statuses", to="live_status.livestatusrule")),
                ("sensor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="live_statuses", to="devices.sensor")),
                ("zone", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="live_statuses", to="farm.zone")),
            ],
            options={
                "db_table": "live_statuses",
                "ordering": ["-raised_at"],
                "verbose_name": "Live Status",
                "verbose_name_plural": "Live Statuses",
            },
        ),
        migrations.AddIndex(
            model_name="livestatus",
            index=models.Index(fields=["farm", "severity", "state"], name="live_statuses_farm_state_idx"),
        ),
        migrations.AddIndex(
            model_name="livestatus",
            index=models.Index(fields=["sensor", "raised_at"], name="live_statuses_sensor_idx"),
        ),
        migrations.AddIndex(
            model_name="livestatus",
            index=models.Index(fields=["state", "raised_at"], name="live_statuses_state_idx"),
        ),
    ]
