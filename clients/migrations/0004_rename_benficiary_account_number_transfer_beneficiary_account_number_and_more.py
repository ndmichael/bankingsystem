# Generated by Django 4.0.4 on 2022-05-16 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_client_gender_transfer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='benficiary_account_number',
            new_name='beneficiary_account_number',
        ),
        migrations.RenameField(
            model_name='transfer',
            old_name='benficiary_bank_address',
            new_name='beneficiary_bank_address',
        ),
    ]
