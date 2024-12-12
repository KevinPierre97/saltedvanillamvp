from django.db import models
from usermodel.models import User


class Review(models.Model):
    """ Model representing a user reviewing a candle """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    candle_id = models.ForeignKey('mymainapp.Candle', on_delete=models.CASCADE, null=True)
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
    # title_text = models.TextField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    isVisible = models.BooleanField(default=True, blank=True)
    isFeatured = models.BooleanField(default=False, blank=True)

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
