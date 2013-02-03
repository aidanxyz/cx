# from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from reviews.models import Feedback, Vote, VoteType
from customauth.models import CustomUser
from items.models import Item
from django.utils import timezone, simplejson

@login_required
@require_POST
def add_feedback(request):
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

@login_required
@require_POST
def vote(request):
	# delete previous vote if such exists
	try:
		v = Vote.objects.get(
			feedback=request.POST['feedback'],
			voted_by=request.user.id,
		).delete()
	except ObjectDoesNotExist as e:
		pass
	# create a vote
	v = Vote(
		feedback=Feedback(id=request.POST['feedback']),
		voted_by=CustomUser(id=request.user.id),
		type=VoteType(id=request.POST['vote_type']),
		date_voted=timezone.now()
	)
	try:
		v.full_clean()
	except ValidationError as e:
		return HttpResponseBadRequest(simplejson.dumps(e.message_dict))
	else:
		assert v.feedback.created_by != request.user.id
		v.save()
		return HttpResponse('vote has been saved')

@login_required
@require_POST
def unvote(request):
	try:
		v = Vote.objects.get(
			feedback=Feedback(id=request.POST['feedback']),
			voted_by=CustomUser(id=request.user.id),
			type=VoteType(id=request.POST['vote_type'])
		).delete()
	except ObjectDoesNotExist as e:
		raise HttpResponseBadRequest("To unvote you must vote first")
	else:
		return HttpResponse('vote has been removed')