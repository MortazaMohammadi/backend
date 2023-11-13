# Generated by Django 4.2.5 on 2023-10-31 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0008_remove_customuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('Employee', 'Employee'), ('Manager', 'Manager'), ('Boss', 'Boss')], default='Agent', max_length=50),
        ),
    ]