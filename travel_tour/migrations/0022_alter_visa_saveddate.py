# Generated by Django 4.2.5 on 2023-12-31 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0021_alter_visa_saveddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visa',
            name='saveddate',
            field=models.DateField(auto_now_add=True),
        ),
    ]
