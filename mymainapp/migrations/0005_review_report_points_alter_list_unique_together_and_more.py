# Generated by Django 4.2.13 on 2024-07-06 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mymainapp', '0004_remove_list_candles_of_list_listitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='report_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='list',
            unique_together={('user_id', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user_id', 'candle_id')},
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_text', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('report_type', models.IntegerField(choices=[(0, 'default'), (1, 'review report')], default=0)),
                ('review_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mymainapp.review')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
