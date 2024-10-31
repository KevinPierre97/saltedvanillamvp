from django.shortcuts import render


def about_view(request):
	""" View function for about page """
	return render(request, 'mymainapp/about/about.html')
