# Generated by Django 4.2.13 on 2024-06-26 23:27

from django.db import migrations, models
import mymainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mymainapp', '0002_review_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='candle',
            name='candle_image',
            field=models.ImageField(blank=True, upload_to=mymainapp.models.Candle.folder_path_candle),
        ),
        migrations.AddField(
            model_name='scentnote',
            name='scentnote_image',
            field=models.ImageField(blank=True, upload_to=mymainapp.models.ScentNote.folder_path_note),
        ),
    ]