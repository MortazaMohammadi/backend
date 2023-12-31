# Generated by Django 4.2.5 on 2023-11-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0012_bill_isprint'),
    ]

    operations = [
        migrations.CreateModel(
            name='qararrdad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('fname', models.CharField(max_length=20)),
                ('passport', models.CharField(max_length=20)),
                ('price', models.FloatField(default='0')),
                ('phone', models.CharField(max_length=12)),
                ('date', models.DateField(auto_now=True)),
                ('payed', models.FloatField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]