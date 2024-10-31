from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView

from mymainapp.forms import CreateCandleModelForm
from mymainapp.models import Candle, Review, List, ListItem


class CandleList_view(generic.ListView):
	model = Candle
	template_name = 'mymainapp/candles/candle_list.html'


@login_required(login_url='/login/')
def candle_list_view(request):
	candle_list = Candle.objects.all()
	paginator = Paginator(candle_list, 30)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'candle_list': candle_list,
		'page_obj': page_obj,
	}
	return render(request, 'mymainapp/candles/candle_list.html', context=context)


@login_required(login_url='/login/')
def candle_detail_view(request, pk):
	""" View function for candle detail page"""
	try:
		candle = Candle.objects.get(pk=pk)
		isReviewed = Review.objects.filter(candle_id=candle, user_id=request.user).exists()
		###################################################################################
		# Checking to see if candle is in any of request.user's lists
		# We are using try,except because there is no getOrNone built into Django
		favorite_list = List.objects.get(user_id=request.user, list_type=4)
		try:
			favorite_item = ListItem.objects.get(list_id=favorite_list, candle_id=candle)
		except ListItem.DoesNotExist:
			favorite_item = None

		have_list = List.objects.get(user_id=request.user, list_type=1)
		try:
			have_item = ListItem.objects.get(list_id=have_list, candle_id=candle)
		except ListItem.DoesNotExist:
			have_item = None

		had_list = List.objects.get(user_id=request.user, list_type=2)
		try:
			had_item = ListItem.objects.get(list_id=had_list, candle_id=candle)
		except ListItem.DoesNotExist:
			had_item = None

		want_list = List.objects.get(user_id=request.user, list_type=3)
		try:
			want_item = ListItem.objects.get(list_id=want_list, candle_id=candle)
		except ListItem.DoesNotExist:
			want_item = None
		####################################################################################

		context = {
			'candle': candle,
			'isReviewed': isReviewed,
			'favorite_item': favorite_item,
			'have_item': have_item,
			'had_item': had_item,
			'want_item': want_item,
		}
	except Candle.DoesNotExist:
		raise Http404('Candle does not exist')

	return render(request, 'mymainapp/candles/candle_detail.html', context=context)


class candle_create_view(SuccessMessageMixin, CreateView):
	model = Candle
	form_class = CreateCandleModelForm
	template_name = 'mymainapp/candles/createcandle_form.html'
	success_message = "Candle: %(name)s was successfully created. Thank you for contributing!"
