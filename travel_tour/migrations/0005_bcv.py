# Generated by Django 4.2.5 on 2023-10-23 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel_tour', '0004_rename_ccv_bill_cv'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.bill')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.customer')),
                ('visa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.visa')),
            ],
        ),
    ]
