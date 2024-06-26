# Generated by Django 4.2.10 on 2024-05-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="is_cancelled",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="is_confirmed",
            field=models.BooleanField(default=True),
        ),
    ]
