# Generated by Django 4.0.4 on 2022-07-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibanking', '0005_remove_bankinghistory_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankinghistory',
            name='amt_aft_charges',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10),
        ),
    ]