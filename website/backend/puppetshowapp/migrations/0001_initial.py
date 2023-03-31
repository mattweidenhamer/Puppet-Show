# Generated by Django 4.1.7 on 2023-03-30 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import puppetshowapp.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DiscordPointingUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email_address"
                    ),
                ),
                ("is_superuser", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Actor",
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
                ("actor_hash", models.UUIDField(default=uuid.uuid4)),
                ("actor_name", models.CharField(max_length=30)),
                (
                    "speaking_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "not_speaking_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "sleeping_animation",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "connection_animation",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "disconnect_animation",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
            ],
            options={
                "db_table": "charactor_actors",
            },
        ),
        migrations.CreateModel(
            name="DiscordData",
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
                ("user_snowflake", models.CharField(max_length=20, unique=True)),
                ("user_username", models.CharField(max_length=100)),
                (
                    "profile_picture",
                    models.ImageField(upload_to=puppetshowapp.models.user_pfp_path),
                ),
            ],
            options={
                "db_table": "discord_user_data",
            },
        ),
        migrations.CreateModel(
            name="Scene",
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
                ("scene_name", models.CharField(max_length=30)),
                (
                    "scene_author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "scenes",
            },
        ),
        migrations.CreateModel(
            name="Emotion",
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
                ("emotion_hash", models.CharField(max_length=200)),
                ("emotion_name", models.CharField(default="Neutral", max_length=15)),
                (
                    "speaking_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "not_speaking_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "sleeping_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "connection_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "disconnect_animation",
                    models.ImageField(upload_to=puppetshowapp.models.user_actor_path),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="puppetshowapp.actor",
                    ),
                ),
            ],
            options={
                "db_table": "character_emotions",
            },
        ),
        migrations.AddField(
            model_name="actor",
            name="actor_base_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="puppetshowapp.discorddata",
            ),
        ),
        migrations.AddField(
            model_name="actor",
            name="scene",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="puppetshowapp.scene"
            ),
        ),
        migrations.AddField(
            model_name="discordpointinguser",
            name="discord_data",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="puppetshowapp.discorddata",
            ),
        ),
    ]
