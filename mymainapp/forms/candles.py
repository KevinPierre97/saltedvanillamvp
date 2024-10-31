from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as s2forms

from mymainapp.models import Brand, Candle


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
