# Generated by Django 5.0.6 on 2024-07-10 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("atlas_trafic_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scorerating",
            name="points",
            field=models.FloatField(default=120),
        ),
    ]
