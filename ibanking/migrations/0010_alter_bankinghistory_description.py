# Generated by Django 4.0.4 on 2022-07-28 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibanking', '0009_bankinghistory_balance_alter_bankinghistory_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankinghistory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
