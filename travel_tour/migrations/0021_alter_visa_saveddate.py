# Generated by Django 4.2.5 on 2023-12-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0020_alter_bill_date_alter_manager_registration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visa',
            name='saveddate',
            field=models.DateField(),
        ),
    ]
