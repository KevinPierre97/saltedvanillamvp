from django.db import models
import uuid
from usermodel.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError


class List(models.Model):
    """ Model representing the lists a user can create/view """

    # when making lists in user save(), make sure to add names to them
    gid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255,
                            blank=True,
                            help_text="The title of the list")
    TYPES_OF_LISTS = (
        (0, 'custom'),
        (1, 'have'),
        (2, 'had'),
        (3, 'want'),
        (4, 'favorites')
    )

    list_type = models.IntegerField(
        choices=TYPES_OF_LISTS,
        default=0
    )

    # candles_of_list = models.ManyToManyField(Candle, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_modified']
        unique_together = ('user_id', 'name')

    def __str__(self):
        """ String representation of the list """
        return f'{self.name} ({self.user_id})'

    def get_absolute_url(self):
        return reverse('list-detail', args=[self.pk])

    def get_or_none(self, **kwargs):
        try:
            return self.objects.get(**kwargs)
        except self.MultipleObjectsReturned as e:
            print('ERR====>', e)

        except self.DoesNotExist:
            return None


def limit_favorites_listitems(value):
    if ListItem.objects.filter(list_id=value, list_id__list_type=4).count() >=3:
    # if ListItem.objects.filter(list_id=value, list_id.list_type=4).count() >=4:
        raise ValidationError('You have reached the maximum number of candles you can add to your favorites list.')


class ListItem(models.Model):
    """ Model representing a single item of a list """
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items', validators=[limit_favorites_listitems,])
    candle_id = models.ForeignKey('mymainapp.Candle', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        unique_together = ('list_id', 'candle_id')
