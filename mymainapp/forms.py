from django import forms
from django.forms import ModelForm
from .models import Brand, Candle, Review, Report, ListItem
from django.urls import reverse_lazy, reverse
from django_select2 import forms as s2forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name',]
        labels = {'name': 'Brand'}
        help_texts = {
            'name': 'Enter the name of a brand not yet added to the catalog. After you click submit, you will go back to the candle list page where you can click +Candle and add a candle with the newly created brand.'
        }


class ScentNotesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ['name__icontains']


class CreateCandleModelForm(ModelForm):
    brand_add_url = reverse_lazy('brand-add-form')
    brand_id = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=True,
        label='Brand',
        help_text=format_html("Add Brand. If the brand is not in the list <a href='{}'>Click Here</a> to add a brand to the list", mark_safe("/brands/add/"))
        # Double check if line above is safe from XSS attacks
    )

    class Meta:
        model = Candle
        fields = ['name', 'brand_id', 'notes', 'candle_image']
        labels = {
            'brand_id': _('Brand'),
            'candle_image': _('Image'),
        }
        help_texts = {
            'brand_id': 'Add Brand. If the brand is not listed, Click Here to add it',
            'candle_image': _('Optional: Upload a photo you took of the candle label'),
            'notes': 'Enter in the fragrance notes sometimes listed on the label of the candle'
        }
        widgets = {
            'notes': ScentNotesWidget
        }


class ReviewCandleModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user_id', 'candle_id', 'rating', 'review_text']
        labels = {
            'user_id': _('Username'),
            'candle_id': _('Candle'),
            'review_text': _('Review'),
        }


class ReportReviewModelForm(ModelForm):

    class Meta:
        model = Report
        fields = ['reporter', 'review_id', 'report_type', 'report_text']
        labels = {
            'reporter': _('User'),
            'report_text': _('Text')
        }
        help_texts = {
            'report_text': _('Describe the content (text,picture,etc) that was offensive and the why (profanity,etc)')
        }
        widgets = {
            'reporter': forms.HiddenInput(),
            'review_id': forms.HiddenInput(),
            'report_type': forms.HiddenInput(),
        }


class ListItemModelForm(ModelForm):

    class Meta:
        model = ListItem
        fields = ['list_id', 'candle_id']
        widgets = {
            'list_id': forms.HiddenInput,
            'candle_id': forms.HiddenInput,
        }