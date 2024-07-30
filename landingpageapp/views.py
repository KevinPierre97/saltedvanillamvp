from django.shortcuts import render
from .forms import MemberForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


def landing_page_view(request):
    context = {}
    return render(request, 'landingpageapp/landing_page.html', context=context)

class landing_page_form_view(SuccessMessageMixin, CreateView):
    form_class = MemberForm
    template_name = 'landingpageapp/landing_page.html'
    success_message = "Thank you for signing up for for the newsletter! We will reach out when updates are available."
    success_url = reverse_lazy('landing-page')