# Generated by Django 4.2.5 on 2023-11-14 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0013_qararrdad'),
    ]

    operations = [
        migrations.AddField(
            model_name='qararrdad',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
