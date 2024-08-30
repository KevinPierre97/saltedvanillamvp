from django.db.models.signals import post_save
from django.dispatch import receiver
from usermodel.models import User
from .models import List


@receiver(post_save, sender=User)
def create_favorites_list(sender, instance, created, **kwargs):
    if created:
        List.objects.create(
            user_id=instance,
            name='favorites',
            list_type=4,
        )
