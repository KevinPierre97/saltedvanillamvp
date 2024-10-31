from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from mymainapp.forms import ListItemModelForm
from mymainapp.models import ListItem, List, Candle
from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin


class listiem_add_create_view(RedirectToPreviousMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = ListItem
	form_class = ListItemModelForm
	# success_message = 'You added %(candle_id)s to your %(list_id.name)s list!'
	template_name = 'mymainapp/lists/listitem_create_form.html'

	def get_initial(self):
		initial = super().get_initial()
		initial['list_id'] = List.objects.get(user_id=self.request.user, list_type=self.kwargs['list_type'])
		initial['candle_id'] = Candle.objects.get(pk=self.kwargs['candle_id'])
		return initial

	def get_context_data(self, **kwargs):
		context=super().get_context_data(**kwargs)
		context["isFavoriteList"] = (self.kwargs['list_type'] == 4)
		return context

	def get_success_message(self, cleaned_data):
		return f'You added {self.object.candle_id} to your {self.object.list_id.name} list!'

	# def form_invalid(self, form):
	# 	context = self.get_context_data(form=form.add_error(ValidationError))
	# 	#raise ValidationError(form.errors)
	# 	return self.render_to_response(context)


class listitem_delete_view(RedirectToPreviousMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = ListItem
	template_name = 'mymainapp/lists/listitem_delete_form.html'
	success_url = reverse_lazy('frontpage')

	def get_success_message(self, cleaned_data):
		return f'You removed {self.object.candle_id} from your {self.object.list_id.name} list!'

	# def form_valid(self, form):
	# 	try:
	# 		self.object.delete()
	# 		# success_message = 'List Item deleted!'
	# 		# messages.success(self.request, self.success_message % {'candle_id': self})
	# 		return HttpResponseRedirect(reverse_lazy('candles'))
	# 	except Exception as e:
	# 		# success_message = 'Error deleting'
	# 		return HttpResponseRedirect(reverse_lazy('candles'))
