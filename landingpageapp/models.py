from django.db import models
from django.utils.translation import gettext_lazy as _


class Member(models.Model):
    """ Model representing a member of Salted Vanilla"""
    email = models.EmailField(
        db_collation='und-x-icu',
        max_length=255,
        unique=True,
        error_messages={
            'unique': _('A member with that email already exists')
        })

    REFERRAL_TYPES = (
        (0, 'default/no referrals'),
        (1, 'r/candles'),
        (2, 'r/luxury candles'),
        (3, 'candle lovers FB page'),
        (4, 'r/django'),
    )

    referred_by = models.IntegerField(
        choices=REFERRAL_TYPES,
        default=0,
        blank=True,
        help_text='This field keeps track of where this member was referred from'
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

