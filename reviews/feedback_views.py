# from django.template import RequestContext, loader
from reviews.models import Feedback
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from customauth.models import CustomUser
from items.models import Item
from django.utils import timezone, simplejson
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add(request):
	f = Feedback(
		body=request.POST['feedback_body'],
		created_by=CustomUser(id=request.user.id),
		date_created=timezone.now(),
		item=Item(id=request.POST['item_id']),
		is_positive=request.POST['is_positive']
	)
	try:
		f.full_clean()
	except ValidationError as e:
		return HttpResponseBadRequest(simplejson.dumps(e.message_dict))
	else:
		f.save()
		return HttpResponse(simplejson.dumps({
			'id': f.id,
			'body': f.body
		}))