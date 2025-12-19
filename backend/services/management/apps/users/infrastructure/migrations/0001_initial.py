from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("role", models.CharField(max_length=32)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
