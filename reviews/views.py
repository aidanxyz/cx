# from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from reviews.models import Feedback, Vote, VoteType
from customauth.models import CustomUser
from items.models import Item
from django.utils import timezone
import json
from django.db.models import F
from reviews.custom_exceptions import WrongVoterException

@login_required
@require_POST
def add_feedback(request, item_id):
	f = Feedback(
		body=request.POST['feedback_body'],
		created_by=CustomUser(id=request.user.id),
		date_created=timezone.now(),
		item=Item(id=item_id),
		is_positive=request.POST['is_positive']
	)
	try:
		f.full_clean()
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	else:
		f.save()
		return HttpResponse(json.dumps({
			'id': f.id,
			'body': f.body,
		}))

@login_required
@require_POST
def vote(request, feedback_id):
	success = {}
	if 'revote' in request.POST:
		# delete previous vote
		try:
			v = Vote.objects.get(feedback=feedback_id, voted_by=request.user.id)
			assert v.type_id != int(request.POST['vote_type']), 'Trying to repeat vote'
			v.delete()
			success['revoted'] = True
		except ObjectDoesNotExist as e:
			pass
	# create a vote
	v = Vote(
		feedback=Feedback(id=feedback_id),
		voted_by=CustomUser(id=request.user.id),
		type=VoteType(id=request.POST['vote_type']),
		date_voted=timezone.now()
	)
	try:
		v.full_clean()
		v.save()
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	except WrongVoterException:
		return HttpResponseBadRequest(json.dumps({'message': "You can't vote for feedback you created"}))
	else:
		success['vote_id'] = v.id
		return HttpResponse(json.dumps(success))

@login_required
@require_POST
def unvote(request, feedback_id):
	try:
		v = Vote.objects.get(
			feedback=feedback_id,
			voted_by=request.user.id,
			type=request.POST['vote_type']
		)
		assert v.voted_by_id == request.user.id
		v.delete()
	except ObjectDoesNotExist as e:
		raise HttpResponseBadRequest("To unvote you must vote first")
	else:
		return HttpResponse(1)