# Generated by Django 4.2.5 on 2023-12-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0019_visa_otherdocs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='registration_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='qararrdad',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='visa',
            name='saveddate',
            field=models.DateField(auto_now_add=True),
        ),
    ]