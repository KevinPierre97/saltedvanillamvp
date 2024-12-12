from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from mymainapp.forms import ReviewCandleModelForm
from mymainapp.models import Review, Candle
from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin


class ReviewList_view(generic.ListView):
	model = Review
	template_name = 'mymainapp/reviews/review_list2.html'


@login_required(login_url='/login/')
def review_list_view(request):
	reviews_list = Review.objects.filter(isVisible=True).order_by('-date_created')
	paginator = Paginator(reviews_list, 30)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'reviews_list': reviews_list,
		'page_obj': page_obj,
	}
	return render(request, 'mymainapp/reviews/review_list.html', context=context) #forgot to add context=context, stuck for an hour


class review_candle_create_view(RedirectToPreviousMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Review
	form_class = ReviewCandleModelForm
	form_class.base_fields['user_id'].disabled = True
	form_class.base_fields['candle_id'].disabled = True
	success_message = "Your review has posted successfully. Thank you for contributing!"
	template_name = 'mymainapp/reviews/review_form.html'

	def get_initial(self):
		initial = super().get_initial()
		initial['user_id'] = self.request.user
		initial['candle_id'] = Candle.objects.get(pk=self.kwargs['candle_id'])
		return initial


class review_candle_update_view(RedirectToPreviousMixin, LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, UpdateView):
	model = Review
	form_class = ReviewCandleModelForm
	form_class.base_fields['user_id'].disabled = True
	form_class.base_fields['candle_id'].disabled = True
	success_message = "Your review has update successfully. Thank you for contributing!"
	template_name = 'mymainapp/reviews/review_form.html'

	def test_func(self):
		review = self.get_object()
		if self.request.user == review.user_id:
			return True
		else:
			return False


class review_candle_delete_view(RedirectToPreviousMixin,LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
	model = Review
	success_message = "Your review has been successfully deleted."
	template_name = 'mymainapp/reviews/review_delete_form.html'

	def test_func(self):
		review = self.get_object()
		if self.request.user == review.user_id:
			return True
		else:
			return False
