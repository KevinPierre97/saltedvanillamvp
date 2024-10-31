from django.db import models
import re


class ScentFamily(models.Model):
    """ Model representing a genre of scent notes"""
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Scent Families'

    def __str__(self):
        return self.name


class ScentGenre(models.Model):
    """ Model representing a genre of scent notes"""
    name = models.CharField(max_length=255, unique=True)
    family = models.ForeignKey(ScentFamily, on_delete=models.CASCADE, null=True, blank=True, related_name='families')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Scent Genres'

    def __str__(self):
        return self.name


class ScentNote(models.Model):
    """ Model representing a scent note """
    name = models.CharField(max_length=255,
                            unique=True,
                            help_text="Name of the scent (use underscores instead of spaces")
    genre = models.ForeignKey(ScentGenre, on_delete=models.SET_NULL, null=True, blank=True, related_name='genres')
    # family = models.ForeignKey(ScentFamily, on_delete=models.SET_NULL, null=True, blank=True)

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
