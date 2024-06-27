# Generated by Django 4.2.13 on 2024-06-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_collation='und-x-icu', error_messages={'unique': 'A member with that email already exists'}, max_length=255, unique=True)),
                ('referred_by', models.IntegerField(blank=True, choices=[(0, 'default/no referrals'), (1, 'r/candles'), (2, 'r/luxury candles'), (3, 'candle lovers FB page'), (4, 'r/django')], default=0, help_text='This field keeps track of where this member was referred from')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
    ]
