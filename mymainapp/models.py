from django.db import models
import uuid
import re
from django.urls import reverse
from usermodel.models import User


class Brand(models.Model):
    """ Model representing a candle maker or brand """
    gid = models.UUIDField(#primary_key=True,
                           default=uuid.uuid4,
                           help_text="Unique ID for this maker")
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', '-date_added']
        verbose_name_plural = 'Makers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('maker-detail', kwargs={'pk': self.id})


class ScentNote(models.Model):
    """ Model representing a scent note """
    name = models.CharField(max_length=255,
                            unique=True,
                            help_text="Name of the scent (use underscores instead of spaces")

    def folder_path_note(self, filename):
        """ Returns the name of the path, which creates a folder for every scent note to store its image"""
        return f"scentnotes/{re.sub('[^0-9a-zA-Z]', '_', self.name)}/{filename}"
    scentnote_image = models.ImageField(upload_to=folder_path_note, blank=True)

    NOTE_TYPE_OPTIONS = (
        ('d', 'Default'),
        ('t', 'Top Note'),
        ('m', 'Middle Note'),
        ('b', 'Base Note'),
    )

    note_type = models.CharField(
        max_length=1,
        choices=NOTE_TYPE_OPTIONS,
        blank=True,
        default='d',
        help_text="Type of Note"
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Scent Notes'

    def __str__(self):
        """ String representation of the scent note """
        return self.name


class Candle(models.Model):
    """ Model representing a candle """
    gid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    brand_id = models.ForeignKey(Brand, on_delete=models.RESTRICT, null=True)
    description = models.TextField(blank=True)
    notes = models.ManyToManyField(ScentNote, blank=True,
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


class Review(models.Model):
    """ Model representing a user reviewing a candle """
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    candle_id = models.ForeignKey(Candle, on_delete=models.CASCADE, null=True)
    RATE_OPTIONS = (
        (0, 'no rate'),
        (1, 'one star'),
        (2, 'two stars'),
        (3, 'three stars'),
        (4, 'four stars'),
        (5, 'five stars')
    )
    rating = models.IntegerField(
        choices=RATE_OPTIONS,
        default=0,
        help_text="With 5 being the best, what do you rate this candle?"
    )

    review_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    isVisible = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['-date_created']
        unique_together = ('user_id', 'candle_id')

    def __str__(self):
        """ String representation of the review """
        return f'{self.user_id} ({self.candle_id.name})'

    report_points = models.IntegerField(default=0, null=False)

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        if self.report_points == 3:
            self.isVisible = False


class Report(models.Model):
    """ Report model """
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    report_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    REPORT_OPTIONS = (
        (0, 'default'),
        (1, 'review report')
    )
    report_type = models.IntegerField(choices=REPORT_OPTIONS, default=0)

    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        """ String representation of the report """
        return f'{self.review_id} ({self.pk})'

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        self.review_id.report_points += 1


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
        (3, 'want')
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


class ListItem(models.Model):
    """ Model representing a single item of a list """
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    candle_id = models.ForeignKey(Candle, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        unique_together = ('list_id', 'candle_id')

