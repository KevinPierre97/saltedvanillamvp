# Generated by Django 4.2.16 on 2024-11-28 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymainapp', '0014_alter_review_user_id_alter_report_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='isFeatured',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]