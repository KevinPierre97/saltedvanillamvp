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
from django.shortcuts import render
from usermodel.models import User
from lockdown.decorators import lockdown
from .models import Brand, Candle, Review
from django.views import generic


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
		context = {
			'candle': candle
		}
	except Candle.DoesNotExist:
		raise Http404('Book does not exist')

	return render(request, 'mymainapp/candle_detail.html', context=context)


def about_view(request):
	""" View function for about page """
	return render(request, 'mymainapp/about.html')

