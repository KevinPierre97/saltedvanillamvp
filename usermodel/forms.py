# Copyright [2021] [FORTH-ICS]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from usermodel.models import User, Profile
from django.contrib.auth import get_user_model

#define user model
User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
	# email = forms.EmailField(required=False) # this didn't work. I just added disable to html field
	class Meta:
		model = User
		fields = ( 'username', )




	# def clean_email(self):
	# 	email = self.cleaned_data['email']
	# 	try:
	# 		account = User.objects.exclude(pk=self.instance.pk).get(email=email)
	# 	except User.DoesNotExist:
	# 		return email
	# 	raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


class ProfileUpdateForm(forms.ModelForm):
	picture = forms.ImageField(label='Profile pic', required=False, error_messages={'invalid': 'Image files only'}, widget=forms.FileInput)
	class Meta:
		model = Profile
		fields = ('picture',)















