# Generated by Django 4.2.13 on 2024-07-07 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mymainapp', '0006_rename_maker_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candle',
            old_name='maker_id',
            new_name='brand_id',
        ),
    ]
