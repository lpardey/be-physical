# Generated by Django 5.0.2 on 2024-02-20 20:32

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_info", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usertrackingpoint",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
