from django.shortcuts import render
from lockdown.decorators import lockdown

from mymainapp.models import Candle, Brand, Review
from usermodel.models import User


@lockdown()
def home_screen_view(request):

	context = {}
	accounts = User.objects.all()
	context['accounts'] = accounts

	return render(request, "mymainapp/front_page/home.html", context)


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

	return render(request, 'mymainapp/front_page/frontpage.html', context=context)
