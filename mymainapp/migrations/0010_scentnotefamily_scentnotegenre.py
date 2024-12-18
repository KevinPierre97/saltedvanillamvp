# Generated by Django 4.2.14 on 2024-08-28 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymainapp', '0009_rename_reporter_report_reporter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScentNoteFamily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Scent Families',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ScentNoteGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Scent Genres',
                'ordering': ['name'],
            },
        ),
    ]
