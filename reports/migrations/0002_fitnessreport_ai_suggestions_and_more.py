# Generated by Django 5.2 on 2025-04-03 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnessreport',
            name='ai_suggestions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='hip_measurement',
            field=models.FloatField(default=80.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='waist_measurement',
            field=models.FloatField(default=94),
            preserve_default=False,
        ),
    ]
