from django import forms
from django.forms import ModelForm

from mymainapp.models import ListItem


class ListItemModelForm(ModelForm):

    class Meta:
        model = ListItem
        fields = ['list_id', 'candle_id']
        widgets = {
            'list_id': forms.HiddenInput,
            'candle_id': forms.HiddenInput,
        }
