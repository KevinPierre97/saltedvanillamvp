# Generated by Django 4.2.17 on 2025-01-14 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mymainapp', '0015_review_isfeatured'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='love_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ReviewLove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mymainapp.review')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'review_id')},
            },
        ),
    ]
