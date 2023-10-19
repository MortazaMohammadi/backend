# Generated by Django 4.2.5 on 2023-10-19 10:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('Employee', 'Employee'), ('Manager', 'Manager'), ('Boss', 'Boss')], default='Agent', max_length=50)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('email', models.CharField(default='unknown', max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('mainstate', models.CharField(max_length=20)),
                ('currentstate', models.CharField(max_length=20)),
                ('passport', models.CharField(max_length=50, null=True)),
                ('profile', models.ImageField(blank=True, upload_to='profile/')),
                ('passportImage', models.ImageField(blank=True, null=True, upload_to='document/')),
                ('cardImage', models.ImageField(blank=True, null=True, upload_to='document/')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_type', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
                ('sell_amount', models.FloatField()),
                ('buy_amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='otherbill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OurEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=60)),
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
            name='Visa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isprocess', models.BooleanField(default=False)),
                ('visapdf', models.FileField(null=True, upload_to='VisaPdfFiles/')),
                ('isapproved', models.BooleanField(default=False)),
                ('isrejected', models.BooleanField(default=False)),
                ('iscomplate', models.BooleanField(default=False)),
                ('saveddate', models.DateField(auto_now=True)),
                ('price', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.customer')),
                ('emailby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.ouremail')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
            ],
        ),
        migrations.CreateModel(
            name='VisaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20)),
                ('duration', models.IntegerField()),
                ('type', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
            ],
        ),
        migrations.CreateModel(
            name='VisaRecivedDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Document', models.CharField(max_length=60, null=True)),
                ('visa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.visa')),
            ],
        ),
        migrations.CreateModel(
            name='visaPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payed', models.FloatField(null=True)),
                ('blockAddress', models.CharField(max_length=50, null=True)),
                ('blockImage', models.ImageField(blank=True, null=True, upload_to='BlockImage/')),
                ('visa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.visa')),
            ],
        ),
        migrations.AddField(
            model_name='visa',
            name='visaType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.visatype'),
        ),
        migrations.CreateModel(
            name='registerPayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payed', models.FloatField(null=True)),
                ('money', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
                ('visa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel_tour.visa')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(max_length=10)),
                ('date', models.DateField()),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.payment_type')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('whatfor', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('پرداخت', 'پرداخت'), ('دریافت', 'دریافت')], default='pay', max_length=50)),
                ('amount', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('registration_date', models.DateField(auto_now=True)),
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
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('reciveddoc', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now=True)),
                ('price', models.FloatField()),
                ('payed', models.FloatField()),
                ('duration', models.IntegerField(null=True)),
                ('isdone', models.BooleanField(default=False)),
                ('money', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel_tour.money')),
                ('othertype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.otherbill')),
                ('visatype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travel_tour.visatype')),
            ],
        ),
    ]
