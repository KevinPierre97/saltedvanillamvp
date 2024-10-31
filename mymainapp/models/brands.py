from django.db import models
import uuid
import re
from django.urls import reverse


class Brand(models.Model):
    """ Model representing a candle maker or brand """
    gid = models.UUIDField(#primary_key=True,
                           default=uuid.uuid4,
                           help_text="Unique ID for this maker")
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', '-date_added']
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand-detail', kwargs={'pk': self.id})


class BrandProfile(models.Model):
    """ Additional information for Brand profile page """
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=200, null=True, blank=True)
    year_founded = models.CharField(max_length=4, null=True, blank=True)

    def folder_path_brand_profile(self, filename):
        return f"brands/{re.sub('[^0-9a-zA-Z]', '_', self.brand_id.name)}/{filename}"
    brand_logo = models.ImageField(upload_to=folder_path_brand_profile, blank=True)

    class Meta:
        verbose_name_plural = 'Brand Profiles'

    def __str__(self):
        return f'{self.brand_id} profile'

