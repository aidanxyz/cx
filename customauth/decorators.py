from django.http import HttpResponse

def login_required_ajax(view_func):
	def _wrapper(request, *args, **kwargs):
		if request.user.is_authenticated():
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponse(status=401)

	return _wrapper