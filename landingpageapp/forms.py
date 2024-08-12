from django import forms
from django.forms import ModelForm
from .models import Member
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class MemberForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Member
        fields = ['email', 'referred_by',]

        widgets = {
            'referred_by': forms.HiddenInput()
        }
