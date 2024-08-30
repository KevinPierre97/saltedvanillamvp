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
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django import forms
from usermodel.models import User
from lockdown.decorators import lockdown

from . import forms
from .forms import BrandForm, CreateCandleModelForm, ReviewCandleModelForm, ReportReviewModelForm
from .models import Brand, Candle, Review, Report, List
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin



@lockdown()
def home_screen_view(request):

	context = {}
	accounts = User.objects.all()
	context['accounts'] = accounts

	return render(request, "mymainapp/home.html", context)


def frontpage_view(request):
	""" View function for front page of Salted Vanilla """
	# Generate counts for main objects
	num_candles = Candle.objects.all().count()
	num_brands = Brand.objects.all().count()
	num_reviews = Review.objects.all().count()

	context = {
		'num_candles': num_candles,
		'num_brands': num_brands,
		'num_reviews': num_reviews,
	}

	return render(request, 'frontpage.html', context=context)


def profile_view(request, usn):
	""" View function for profile pages """
	profile = User.objects.get(username=usn)
	reviews_List = Review.objects.filter(user_id=profile, isVisible=True)
	try:
		favorites_list = List.objects.get(user_id=profile, list_type=4)
	except List.DoesNotExist:
		favorites_list = None


	context = {
		'profile': profile,
		'reviews_List': reviews_List,
		'favorites_list': favorites_list,
	}
	return render(request, 'mymainapp/profile.html', context=context)

class CandleList_view(generic.ListView):
	model = Candle
	template_name = 'mymainapp/candle_list.html'


class ReviewList_view(generic.ListView):
	model = Review
	template_name = 'mymainapp/review_list.html'

def candle_list_view(request):
	candle_list = Candle.objects.all()
	context = {
		'candle_list': candle_list
	}
	return render(request, 'mymainapp/candle_list.html', context=context)


def candle_detail_view(request, pk):
	""" View function for candle detail page"""
	try:
		candle = Candle.objects.get(pk=pk)
		isReviewed = Review.objects.filter(candle_id=candle, user_id=request.user).exists()
		context = {
			'candle': candle,
			'isReviewed': isReviewed,
		}
	except Candle.DoesNotExist:
		raise Http404('Book does not exist')

	return render(request, 'mymainapp/candle_detail.html', context=context)


def about_view(request):
	""" View function for about page """
	return render(request, 'mymainapp/about.html')





class candle_create_view(SuccessMessageMixin, CreateView):
	model = Candle
	form_class = CreateCandleModelForm
	template_name = 'mymainapp/createcandle_form.html'
	success_message = "Candle: %(name)s was successfully created. Thank you for contributing!"


class RedirectToPreviousMixin:
	default_redirect = '/home'

	def get(self, request, *args, **kwargs):
		request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
		return super().get(request, *args, **kwargs)
	def get_success_url(self):
		return self.request.session['previous_page']


class brand_create_view(RedirectToPreviousMixin, SuccessMessageMixin, CreateView):
	model = Brand
	form_class = BrandForm
	# fields = ('name',)
	template_name = 'mymainapp/brand_form.html'
	success_message = "Brand: %(name)s was successfully created"
	success_url = reverse_lazy('frontpage')


class review_candle_create_view(RedirectToPreviousMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Review
	form_class = ReviewCandleModelForm
	form_class.base_fields['user_id'].disabled = True
	form_class.base_fields['candle_id'].disabled = True
	success_message = "Your review has posted successfully. Thank you for contributing!"
	template_name = 'mymainapp/review_form.html'

	def get_initial(self):
		initial = super().get_initial()
		initial['user_id'] = self.request.user
		initial['candle_id'] = Candle.objects.get(pk=self.kwargs['candle_id'])
		return initial


class report_review_create_view(RedirectToPreviousMixin, CreateView):
	model = Report
	form_class = ReportReviewModelForm

	# This section makes the default information disable so users don't have to put in that effort
	# and so html attacks won't work
	form_class.base_fields['reporter'].disabled = True
	form_class.base_fields['review_id'].disabled = True
	form_class.base_fields['report_type'].disabled = True
	template_name = 'mymainapp/report_review_form.html'

	# this function defines initial values
	def get_initial(self):
		initial = super().get_initial()
		initial['reporter'] = self.request.user
		initial['review_id'] = Review.objects.get(pk=self.kwargs['review_id'])
		initial['report_type'] = self.kwargs['report_type_id']
		return initial

	#this function is to pass the review to display on form page
	def get_context_data(self, **kwargs):
		context = super(report_review_create_view, self).get_context_data(**kwargs)
		context['review'] = Review.objects.get(pk=self.kwargs['review_id'])
		return context

	#this function is to hid the default fields to not confuse users
	# def get_form(self, form_class=None):
	# 	form = super().get_form(form_class)
	# 	form.fields['reporter'].widget = forms.HiddenInput()

