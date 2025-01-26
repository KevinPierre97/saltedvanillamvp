from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.shortcuts import render

from mymainapp.models.likes_and_notifications import Notification
from mymainapp.views.redirectpreviousmixin import RedirectToPreviousMixin
from mymainapp.models import ReviewLike, Review
from mymainapp.forms import ReviewLikeModelForm


class reviewlike_create_view(LoginRequiredMixin, RedirectToPreviousMixin, SuccessMessageMixin, CreateView):
    model = ReviewLike
    form_class = ReviewLikeModelForm
    success_message = "Thanks for spreading love!"
    template_name = 'mymainapp/likes_and_notifications/reviewlike_create_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['user_id'] = self.request.user
        initial['review_id'] = Review.objects.get(pk=self.kwargs['review_id_pk'])
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        review_instance = Review.objects.get(pk=self.kwargs['review_id_pk'])
        review_instance.liked()
        Notification.objects.create(
            recipient=review_instance.user_id,
            message=f'{self.request.user.username} liked your {review_instance.candle_id} review!'
        )
        return response


def notifications_view(request):
    user = request.user
    notification_list = Notification.objects.filter(recipient=user)
    context = {
        'notification_list': notification_list,
    }
    # Decoupled response and return to add change all notifications to read after page is generated
    response = render(request, 'mymainapp/likes_and_notifications/notifications.html', context=context)
    notification_list.update(is_read=True)
    return response

