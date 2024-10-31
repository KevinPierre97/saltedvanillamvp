from django.db import models
import uuid
import re
from django.urls import reverse


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

    def __str__(self):
        """ String representation of the candle """
        return f'{self.name} ({self.brand_id.name})'

    def get_absolute_url(self):
        return reverse('candle-detail', kwargs={'pk': self.id})
