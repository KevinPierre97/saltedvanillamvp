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

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from usermodel.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfileUpdateForm
from usermodel.models import Profile


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'usermodel/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/candles')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("/candles")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("frontpage")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "usermodel/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		# email1 = request.user.email
		account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if account_form.is_valid() and profile_form.is_valid():
			account_form.initial = {
					# "email": request.POST['email'],
					"username": request.POST['username'],
			}
			profile_form.save()
			profile = Profile.objects.get(user_id=request.user)
			profile.new_picture()
			hello = account_form.save(commit=False)
			# hello.email = email1
			hello.save()
			context['success_message'] = "Updated"
	else:
		account_form = AccountUpdateForm(

			initial={
					# "email": request.user.email,
					"username": request.user.username,
				}
			)
		profile_form = ProfileUpdateForm(instance=request.user.profile)

	context['account_form'] = account_form
	context['profile_form'] = profile_form
	return render(request, "usermodel/account.html", context)

