from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render
from customauth.models import CustomUser, CustomUserRegistrationForm

def register_user(request):
	if request.user.is_authenticated():
		return HttpResponseForbidden()

	if request.method == "POST":
		form = CustomUserRegistrationForm(request.POST)
		if form.is_valid():
			user = CustomUser.objects.create_user(
				form.cleaned_data.get('email'),
				form.cleaned_data.get('full_name'),
				form.cleaned_data.get('year_of_birth'),
				form.cleaned_data.get('gender'),
				form.cleaned_data.get('country'),
				form.cleaned_data.get('password')
			)
			return HttpResponseRedirect(reverse('items.views.explore'))
	else:
		form = CustomUserRegistrationForm()

	return render(request, 'customauth/register.html', {
		'form': form,
		})
