# Generated by Django 5.2 on 2025-04-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_fitnessreport_ai_suggestions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='hip_measurement',
            field=models.FloatField(default=90.0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='waist_measurement',
            field=models.FloatField(default=80.0),
        ),
    ]
