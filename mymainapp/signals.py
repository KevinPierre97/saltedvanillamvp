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


@receiver(post_save, sender=Review)
def update_candle_date_modified(sender, instance, created, **kwargs):
    if created:
        candle = Candle.objects.get(
            pk=instance.candle_id.pk
        )
        candle.save()