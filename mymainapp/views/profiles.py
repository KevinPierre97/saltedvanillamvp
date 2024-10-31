from django.shortcuts import render

from mymainapp.models import Review, List
from usermodel.models import User


def profile_view(request, usn):
	""" View function for profile pages """
	profile = User.objects.get(username=usn)
	reviews_List = Review.objects.filter(user_id=profile, isVisible=True)

	############# Importing all listss ################################
	#If all lists are created with user create signal, then there is no need for try,except#
	try:
		favorites_list = List.objects.get(user_id=profile, list_type=4)
	except List.DoesNotExist:
		favorites_list = None
	try:
		have_list = List.objects.get(user_id=profile, list_type=1)
	except List.DoesNotExist:
		have_list = None
	try:
		want_list = List.objects.get(user_id=profile, list_type=3)
	except List.DoesNotExist:
		want_list = None
	try:
		had_list = List.objects.get(user_id=profile, list_type=2)
	except List.DoesNotExist:
		had_list = None
	####################################################################

	context = {
		'profile': profile,
		'reviews_List': reviews_List,
		'favorites_list': favorites_list,
		'have_list': have_list,
		'want_list': want_list,
		'had_list': had_list,

	}
	return render(request, 'mymainapp/profiles/profile.html', context=context)
