# Generated by Django 5.0.3 on 2024-04-19 17:29

import datetime

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user_info", "0002_alter_userinfo_birth_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Diet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
        ),
        migrations.CreateModel(
            name="Equipment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Muscle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=100)),
                ("action", models.CharField(max_length=100)),
                (
                    "muscle_group",
                    models.IntegerField(
                        choices=[
                            (0, "Neck"),
                            (1, "Back"),
                            (2, "Shoulder"),
                            (3, "Arm"),
                            (4, "Wrist"),
                            (5, "Hand"),
                            (6, "Abdomen"),
                            (7, "Hip"),
                            (8, "Upper_Leg_And_Knee"),
                            (9, "Lower_Leg_And_Foot"),
                            (10, "Special"),
                        ],
                        default=8,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, max_length=144)),
                (
                    "difficulty_level",
                    models.IntegerField(
                        choices=[(0, "Beginner"), (1, "Intermediate"), (2, "Advanced"), (3, "Special")], default=0
                    ),
                ),
                ("repetition_duration", models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("image_url", models.URLField()),
                ("video_url", models.URLField()),
                ("equipment", models.ManyToManyField(to="training.equipment")),
                (
                    "tracking_label",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="user_info.usertrackinglabel"),
                ),
                ("muscles", models.ManyToManyField(related_name="exercises", to="training.muscle")),
            ],
        ),
        migrations.CreateModel(
            name="Training",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("type", models.CharField(blank=True, max_length=50)),
                ("start_date", models.DateField(default=datetime.date.today)),
                (
                    "due_date",
                    models.DateField(
                        validators=[
                            django.core.validators.MinValueValidator(models.DateField(default=datetime.date.today))
                        ]
                    ),
                ),
                ("user_info", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="user_info.userinfo")),
            ],
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, max_length=144)),
                (
                    "difficulty_level",
                    models.IntegerField(
                        choices=[(0, "Beginner"), (1, "Intermediate"), (2, "Advanced"), (3, "Special")], default=0
                    ),
                ),
                (
                    "intensity",
                    models.IntegerField(
                        choices=[(0, "Low"), (1, "Intermediate"), (2, "High"), (3, "Special")], default=0
                    ),
                ),
                (
                    "training",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="workouts", to="training.training"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Routine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("workout_index", models.IntegerField()),
                ("sets", models.IntegerField()),
                ("repetitions", models.IntegerField()),
                ("sets_rest", models.IntegerField()),
                ("routine_rest", models.IntegerField()),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="routines", to="training.exercise"
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="routines", to="training.workout"
                    ),
                ),
            ],
        ),
    ]