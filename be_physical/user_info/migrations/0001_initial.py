# Generated by Django 5.0.2 on 2024-03-01 17:53

import datetime

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Height in meters",
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(1.0),
                            django.core.validators.MaxValueValidator(2.5),
                        ],
                    ),
                ),
                ("birth_date", models.DateField(help_text="Birthdate as day/month/year")),
            ],
        ),
        migrations.CreateModel(
            name="UserTrackingLabel",
            fields=[
                ("label", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("description", models.TextField(blank=True, max_length=144)),
            ],
        ),
        migrations.CreateModel(
            name="UserAnnotation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(max_length=500)),
                (
                    "annotation_type",
                    models.IntegerField(
                        choices=[(0, "General"), (1, "Goal"), (2, "Restriction"), (3, "Trainer Annotation")], default=0
                    ),
                ),
                ("scope", models.IntegerField(choices=[(0, "User"), (1, "Trainer")], default=0)),
                ("status", models.IntegerField(choices=[(0, "Inactive"), (1, "Active")], default=1)),
                (
                    "user_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="annotations",
                        to="user_info.userinfo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTrackingPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=datetime.date.today)),
                ("value", models.FloatField()),
                (
                    "label",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="user_info.usertrackinglabel"),
                ),
                (
                    "user_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracking_points",
                        to="user_info.userinfo",
                    ),
                ),
            ],
        ),
    ]
