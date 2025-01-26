from django.forms import ModelForm

from django import forms
from mymainapp.models import ReviewLike


class ReviewLikeModelForm(ModelForm):
    class Meta:
        model = ReviewLike
        fields = ['user_id', 'review_id']
        widgets = {
            'user_id': forms.HiddenInput(),
            'review_id': forms.HiddenInput()
        }
