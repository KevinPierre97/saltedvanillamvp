# Generated by Django 4.2.13 on 2024-06-26 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]