from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from mymainapp.models import Report


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
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Error: You have already submitted a report for this review'
            }
        }
