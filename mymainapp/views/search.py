from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mymainapp.filters import CandleFilter
from mymainapp.models import Candle


@login_required(login_url='/login/')
def candle_filter_search(request):
	filtered = CandleFilter(request.GET, queryset=Candle.objects.all())
	# paginator = Paginator(filtered.qs, 9)
	# page_number = request.GET.get('page')
	# page_obj = paginator.get_page(page_number)
	# try:
	# 	page_obj = paginator.page(page_number)
	# except PageNotAnInteger:
	# 	page_obj = paginator.page(1)
	# except EmptyPage:
	# 	page_obj = paginator.page(paginator.num_pages)

	context = {
		#'request': request,
		'filter': filtered,
		#'page_obj': page_obj,
	}
	return render(request, 'mymainapp/search/candle_filter_search.html', context=context)
