# from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from customauth.decorators import login_required_ajax
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from reviews.models import Feedback, Vote, VoteType, Detail, DetailAddForm
from customauth.models import CustomUser
from items.models import Item
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

@login_required_ajax
@require_POST
def add_feedback(request, item_id):
	f = Feedback(
		body=request.POST.get('feedback_body'),
		created_by=CustomUser(id=request.user.id),
		date_created=timezone.now(),
		item=Item(id=item_id),
		is_positive=request.POST.get('is_positive')
	)
	try:
		f.full_clean()
		f.save(request=request)
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	except Exception as e:
		return HttpResponseBadRequest(json.dumps({'message': e.value}))
	else:
		return HttpResponse(json.dumps({
			'id': f.id,
			'body': f.body,
		}))

@login_required_ajax
@require_POST
def vote(request, feedback_id):
	success = {}
	if 'revote' in request.POST and request.POST['revote']:
		# delete previous vote
		try:
			v = Vote.objects.get(feedback=feedback_id, voted_by=request.user.id)
			assert v.type_id != int(request.POST['vote_type']), 'Trying to repeat vote'
			v.delete()
			success['revoted'] = True
		except ObjectDoesNotExist as e:
			pass # means frontend problem
	# create a vote
	v = Vote(
		feedback=Feedback(id=feedback_id),
		voted_by=CustomUser(id=request.user.id),
		type=VoteType(id=request.POST.get('vote_type')),
		date_voted=timezone.now()
	)
	try:
		v.full_clean()
		v.save(request=request)
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	except Exception as e:
		return HttpResponseBadRequest(json.dumps({'message': e.value}))
	else:
		success['vote_id'] = v.id
		return HttpResponse(json.dumps(success))

@login_required_ajax
@require_POST
def unvote(request, feedback_id):
	try:
		v = Vote.objects.get(
			feedback=feedback_id,
			voted_by=request.user.id,
			type=request.POST.get('vote_type')
		)
		assert v.voted_by_id == request.user.id
		v.delete()
	except ObjectDoesNotExist as e:
		raise HttpResponseBadRequest("To unvote you must vote first")
	else:
		return HttpResponse(1)

@require_POST
@login_required_ajax
def add_detail(request, feedback_id):
	d = Detail(
		body=request.POST.get('body'),
		feedback=Feedback(id=feedback_id),
		written_by=CustomUser(id=request.user.id),
		date_written=timezone.now()
	)
	try:
		d.full_clean()
		d.save(request=request)
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	except Exception as e:
		return HttpResponseBadRequest(json.dumps({'message': e.value}))
	else:
		return HttpResponse(json.dumps({
			'id': d.id,
			'date_written': d.date_written,
			'written_by': request.user.full_name,
			'body': d.body,
		}, cls=DjangoJSONEncoder))

def list_details(request, feedback_id):
	page = request.GET.get('page')
	if not page:
		page = 1
	# else:
	# 	page = int(page)
	feedback = Feedback.objects.get(pk=feedback_id)
	details = Detail.objects.filter(feedback=feedback_id)
	paginator = Paginator(details, settings.DETAILS_PER_PAGE)
	try:
		details_range = paginator.page(page)
	except EmptyPage:
		# If page is out of range
		details_range = paginator.range(paginator.num_pages)
	return render(request, 'reviews/details/list.html', {
		'feedback': feedback,
		'details': details_range,
	})