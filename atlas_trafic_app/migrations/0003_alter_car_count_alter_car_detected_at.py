# Generated by Django 5.0.6 on 2024-07-22 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("atlas_trafic_app", "0002_car"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="car",
            name="detected_at",
            field=models.DateTimeField(),
        ),
    ]
