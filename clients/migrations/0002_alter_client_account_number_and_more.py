# Generated by Django 4.0.4 on 2022-05-09 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='account_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='transfer_pin',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
