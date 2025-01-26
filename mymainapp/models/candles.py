from django.db import models
import uuid
import re
from django.urls import reverse
from usermodel.models import User


class Candle(models.Model):
    """ Model representing a candle """
    gid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    brand_id = models.ForeignKey('mymainapp.Brand', on_delete=models.RESTRICT, null=True)
    description = models.TextField(blank=True)
    notes = models.ManyToManyField('mymainapp.ScentNote', blank=True,
                                   help_text="Enter in the fragrance notes listed on the label of the candle")

    def folder_path_candle(self, filename):
        # return f'{self.maker_id.name.replace(" ", "_")}/{self.name.replace(" ", "_")}/{filename}'
        return f"candles/{re.sub('[^0-9a-zA-Z]', '_', self.brand_id.name)}/{re.sub('[^0-9a-zA-Z]', '_', self.name)}/{filename}"
    candle_image = models.ImageField(upload_to=folder_path_candle, blank=True)

    isImageAdminApproved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_modified']
        verbose_name_plural = 'Candles'

    @property
    def get_average_cold_throw_rating(self):
        return self.candleexperiencevote_set.aggregate(average=models.Avg('cold_throw_rating'))['average']

    @property
    def get_average_warm_throw_rating(self):
        return self.candleexperiencevote_set.aggregate(average=models.Avg('warm_throw_rating'))['average']

    def __str__(self):
        """ String representation of the candle """
        return f'{self.name} ({self.brand_id.name})'

    def get_absolute_url(self):
        return reverse('candle-detail', kwargs={'pk': self.id})


class CandleExperienceVote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    candle_id = models.ForeignKey(Candle, on_delete=models.CASCADE)
    RATE_OPTIONS = (
        (0, 'no rate'),
        (1, 'low'),
        (2, 'medium'),
        (3, 'high')
    )
    cold_throw_rating = models.IntegerField(choices=RATE_OPTIONS,
                                            default=0,
                                            help_text="Vote on how strong candle scent is while not burning")
    warm_throw_rating = models.IntegerField(choices=RATE_OPTIONS,
                                            default=0,
                                            help_text="Vote on how strong candle scent is while burning")
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']
        unique_together = ('user_id', 'candle_id')

    def __str__(self):
        return f'{self.user_id} - {self.candle_id} Vote'
