from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import CreateView

from mymainapp.forms import BrandForm
from mymainapp.models import Brand, Candle
from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin


class brand_create_view(RedirectToPreviousMixin, SuccessMessageMixin, CreateView):
	model = Brand
	form_class = BrandForm
	# fields = ('name',)
	template_name = 'mymainapp/brands/brand_form.html'
	success_message = "Brand: %(name)s was successfully created"
	success_url = reverse_lazy('frontpage')


def brand_detail_view(request, pk):
	""" View to display all the candles of a brand """
	try:
		brand = Brand.objects.get(pk=pk)
		candle_list = Candle.objects.filter(brand_id__pk=pk)
		paginator = Paginator(candle_list, 30)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		if brand.profile.all():
			context = {
				'brand': brand,
				'candle_list': candle_list,
				'page_obj': page_obj
			}
			return render(request, 'mymainapp/brands/brand_detail.html', context=context)
		else:
			context = {
				'brand': brand,
				'candle_list': candle_list,
				'page_obj': page_obj,
			}
			return render(request, 'mymainapp/brands/brand_detail_no_profile.html', context=context)
	except Brand.DoesNotExist:
		raise Http404('Brand does not exist')