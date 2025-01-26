from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from mymainapp.forms import ReportReviewModelForm
from mymainapp.models import Report, Review
from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin


class report_review_create_view(RedirectToPreviousMixin, SuccessMessageMixin, CreateView):
	model = Report
	form_class = ReportReviewModelForm
	success_message = "Your report has been submitted! A moderator will review it shortly."

	# This section makes the default information disable so users don't have to put in that effort
	# and so html attacks won't work
	form_class.base_fields['reporter'].disabled = True
	form_class.base_fields['review_id'].disabled = True
	form_class.base_fields['report_type'].disabled = True
	template_name = 'mymainapp/reports/report_review_form.html'

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

	def form_valid(self, form):
		response = super().form_valid(form)
		review_instance = Review.objects.get(pk=self.kwargs['review_id'])
		review_instance.reported()
		return response
