# Generated by Django 4.0.4 on 2022-05-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_remove_transfer_transfer_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='IBAN',
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
    ]
