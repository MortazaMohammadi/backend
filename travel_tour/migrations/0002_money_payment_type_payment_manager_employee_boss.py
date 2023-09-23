# Generated by Django 4.2.5 on 2023-09-20 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_type', models.CharField(max_length=5)),
                ('amount', models.IntegerField()),
                ('sell_amount', models.FloatField()),
                ('buy_amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.payment_type')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=50)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=50)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('registeration_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.CharField(max_length=50)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]