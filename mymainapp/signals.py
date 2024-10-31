from django.db.models.signals import post_save
from django.dispatch import receiver
from usermodel.models import User
from .models import List, Review, Candle
import datetime


@receiver(post_save, sender=User)
def create_favorites_list(sender, instance, created, **kwargs):
    if created:
        List.objects.create(
            user_id=instance,
            name='favorites',
            list_type=4,
        )
        List.objects.create(
            user_id=instance,
            name='had',
            list_type=2
        )
        List.objects.create(
            user_id=instance,
            name='want',
            list_type=3,
        )
        List.objects.create(
            user_id=instance,
            name='have',
            list_type=1
        )


@receiver(post_save, sender=Review)
def update_candle_date_modified(sender, instance, created, **kwargs):
    if created:
        candle = Candle.objects.get(
            pk=instance.candle_id.pk
        )
        candle.save()

# Possibly add another update when a list item is created
