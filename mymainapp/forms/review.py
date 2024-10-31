from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from mymainapp.models import Review


class ReviewCandleModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user_id', 'candle_id', 'rating', 'review_text']
        labels = {
            'user_id': _('Username'),
            'candle_id': _('Candle'),
            'review_text': _('Review'),
        }
