from django.db import models
from usermodel.models import User


class Report(models.Model):
    """ Report model """
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review_id = models.ForeignKey('mymainapp.Review', on_delete=models.CASCADE, null=True, blank=True)

    report_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    REPORT_OPTIONS = (
        (0, 'default'),
        (1, 'review report')
    )
    report_type = models.IntegerField(choices=REPORT_OPTIONS, default=0)
    isReviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']
        unique_together =('reporter', 'review_id')

    def __str__(self):
        """ String representation of the report """
        return f'{self.review_id} ({self.pk})'

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        self.review_id.report_points += 1
