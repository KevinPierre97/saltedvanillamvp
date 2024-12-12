from django.shortcuts import render
from lockdown.decorators import lockdown
from django.contrib.auth.decorators import login_required

from mymainapp.models import Candle, Brand, Review
from usermodel.models import User


@lockdown()
def home_screen_view(request):

	context = {}
	accounts = User.objects.all()
	context['accounts'] = accounts

	return render(request, "mymainapp/front_page/home.html", context)


@login_required(login_url='/login/')
def frontpage_view(request):
	""" View function for front page of Salted Vanilla """
	# Generate counts for main objects
	num_candles = Candle.objects.all().count()
	num_brands = Brand.objects.all().count()
	num_reviews = Review.objects.all().count()
	num_accounts = User.objects.all().count()
	featured_reviews = Review.objects.filter(isFeatured=True)[:3]
	recently_added_candles = Candle.objects.all().order_by('-date_added')[:6]

	context = {
		'num_candles': num_candles,
		'num_brands': num_brands,
		'num_reviews': num_reviews,
		'num_accounts': num_accounts,
		'featured_reviews': featured_reviews,
		'recently_added_candles': recently_added_candles,
	}

	return render(request, 'mymainapp/front_page/frontpage_20241128.html', context=context)
