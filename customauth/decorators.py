from django.http import HttpResponse

def login_required_ajax(view_func):
	def decorator_logic(request, *args, **kwargs):
		if request.user.is_authenticated():
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponse(status=401)

	return decorator_logic

def permission_required(codename):
	def decorator(view_func):
		def decorator_logic(request, *args, **kwargs):
			if request.user.has_perm(codename):
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse(status=403)
		return decorator_logic
	return decorator