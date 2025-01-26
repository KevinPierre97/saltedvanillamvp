from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView, UpdateView
from django.db.models import Exists, OuterRef

from mymainapp.forms import CreateCandleModelForm, CandleExperienceVoteModelForm
from mymainapp.models import Candle, CandleExperienceVote, Review, List, ListItem, ReviewLike

from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin


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
		reviews_list = Review.objects.filter(candle_id=candle).annotate(
			is_liked=Exists(ReviewLike.objects.filter(user_id=request.user, review_id=OuterRef('id')))
		)
		experience_vote_count = CandleExperienceVote.objects.filter(candle_id=candle).count()
		try:
			user_experience_vote = CandleExperienceVote.objects.get(user_id=request.user, candle_id=candle)
		except CandleExperienceVote.DoesNotExist:
			user_experience_vote = None
		####################################################################################

		context = {
			'candle': candle,
			'isReviewed': isReviewed,
			'favorite_item': favorite_item,
			'have_item': have_item,
			'had_item': had_item,
			'want_item': want_item,
			'reviews_list': reviews_list,
			'experience_vote_count': experience_vote_count,
			'user_experience_vote': user_experience_vote,
		}
	except Candle.DoesNotExist:
		raise Http404('Candle does not exist')

	return render(request, 'mymainapp/candles/candle_detail.html', context=context)


class candle_create_view(SuccessMessageMixin, LoginRequiredMixin,CreateView):
	model = Candle
	form_class = CreateCandleModelForm
	template_name = 'mymainapp/candles/createcandle_form.html'
	success_message = "Candle: %(name)s was successfully created. Thank you for contributing!"


class candle_experience_vote_create_view(SuccessMessageMixin, LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
	model = CandleExperienceVote
	form_class = CandleExperienceVoteModelForm
	form_class.base_fields['user_id'].disabled = True
	form_class.base_fields['candle_id'].disabled = True
	success_message = 'Your vote has uploaded successfully. Thank you for contributing!'
	template_name = 'mymainapp/candles/candle_experience_vote_form.html'

	def get_initial(self):
		initial = super().get_initial()
		initial['user_id'] = self.request.user
		initial['candle_id'] = Candle.objects.get(pk=self.kwargs['candle_id'])
		return initial

class candle_experience_vote_update_view(SuccessMessageMixin, LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
	model = CandleExperienceVote
	form_class = CandleExperienceVoteModelForm
	form_class.base_fields['user_id'].disabled = True
	form_class.base_fields['candle_id'].disabled = True
	success_message = 'Your vote has updated successfully. Thank you for contributing!'
	template_name = 'mymainapp/candles/candle_experience_vote_form.html'

	def test_func(self):
		candle_experience_vote = self.get_object()
		if self.request.user == candle_experience_vote.user_id:
			return True
		else:
			return False