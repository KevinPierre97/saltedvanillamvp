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

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

#These are added for the get_password_reset_url function
from django import utils
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
import re


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(
		db_collation='und-x-icu',
		max_length=255,
		unique=True,
		error_messages={
			'unique': _('A user with such email already exists')
		}
	)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(
		_('Date Joined'),
		default=timezone.now
	)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_staff = models.BooleanField(
		_('Staff Status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.')
	)
	is_active = models.BooleanField(
		_('Active'),
		default=True,
		help_text=_('Designates whether this user should be treated as active.')
	)
	is_superuser			= models.BooleanField(default=False)
	is_email_confirmed = models.BooleanField(
		_('Email Confirmed'),
		default=False
	)

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	class Meta:
		verbose_name = _('User')
		verbose_name_plural = _('Users')

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_staff

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, recipient_list=[self.email], **kwargs)

	def get_password_reset_url(self):
		base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(self.pk))
		token = PasswordResetTokenGenerator().make_token(self)
		reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
		reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
		reset_url = f'{settings.BASE_URL}{reset_path}'
		return reset_url


class Profile(models.Model):
	user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
	bio = models.TextField()

	def profile_picture_path(self, filename):
		return f"profiles/{re.sub('[^0-9a-zA-Z]', '_', str(self.user_id.id))}/{filename}"

	picture = models.ImageField(upload_to=profile_picture_path, default='defaults/logo.png', null=True, blank=True)
	# default_picture never changes, it's my first idea to prevent users from using whatever they want as a profile pic
	# the idea is, when a user changes their picture field, their profile picture will default_picture until admin approval
	default_picture = models.ImageField(upload_to=profile_picture_path, default='defaults/logo.png', null=True, blank=True)
	isPictureUpdated = models.BooleanField(default=False)
	isPictureApproved = models.BooleanField(default=True)

	def new_picture(self):
		self.isPictureUpdated = True
		self.isPictureApproved = False
		self.save()

	def __str__(self):
		return f'{self.user_id} Profile'
