# Generated by Django 4.2.5 on 2023-10-26 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0005_bcv'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherbill',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]