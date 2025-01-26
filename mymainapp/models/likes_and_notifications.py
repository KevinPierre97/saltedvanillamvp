from django.db import models
from usermodel.models import User


class ReviewLike(models.Model):
    # user_id is user who loved the review
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.ForeignKey('mymainapp.Review', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'review_id')


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)