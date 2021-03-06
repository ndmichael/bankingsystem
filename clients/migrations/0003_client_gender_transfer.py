# Generated by Django 4.0.4 on 2022-05-11 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0002_alter_client_account_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], default='male', max_length=7),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(default='US DOLLAR', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('IBAN', models.CharField(max_length=34)),
                ('receivers_name', models.CharField(max_length=50)),
                ('benficiary_account_number', models.CharField(max_length=10)),
                ('benficiary_bank_address', models.TextField()),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('dotf', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_success', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
