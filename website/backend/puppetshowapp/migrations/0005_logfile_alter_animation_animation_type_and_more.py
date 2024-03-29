# Generated by Django 4.1.7 on 2023-05-14 14:14

from django.db import migrations, models
import puppetshowapp.models.data_models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("puppetshowapp", "0004_remove_uuid_null"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "log_type",
                    models.CharField(
                        choices=[
                            ("INFO", "Info"),
                            ("WARNING", "Warning"),
                            ("ERROR", "Error"),
                            ("CRITICAL", "Critical"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "log_file",
                    models.FileField(
                        upload_to=puppetshowapp.models.data_models.default_log_location
                    ),
                ),
            ],
            options={
                "db_table": "log_files",
            },
        ),
        migrations.AlterField(
            model_name="animation",
            name="animation_type",
            field=models.CharField(
                choices=[
                    ("START_SPEAKING", "Start Speaking"),
                    ("NOT_SPEAKING", "Stop Speaking"),
                    ("SLEEPING", "Sleeping"),
                    ("CONNECTION", "Connection"),
                    ("DISCONNECTION", "Disconnect"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="animation",
            name="identifier",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
