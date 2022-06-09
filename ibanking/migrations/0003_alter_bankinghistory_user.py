# Generated by Django 4.0.4 on 2022-06-09 01:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ibanking', '0002_alter_bankinghistory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankinghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL),
        ),
    ]
