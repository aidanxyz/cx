# from django.template import RequestContext, loader
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from customauth.decorators import login_required_ajax, permission_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from reviews.models import *
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
import MySQLdb
from contextlib import closing
from django.shortcuts import render, get_object_or_404

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
	if 'is_revote' in request.POST and request.POST['is_revote']:
		# delete previous vote
		try:
			v = Vote.objects.get(feedback=feedback_id, voted_by=request.user.id)
			print v
			assert v.type_id != int(request.POST['vote_type']), 'Trying to repeat vote'
			v.delete()
			success['revoted'] = True
		except ObjectDoesNotExist as e:
			# TODO: log it, email to support etc.
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
		return HttpResponseBadRequest("To unvote you must vote first")
	else:
		return HttpResponse(1)

@require_POST
#@login_required_ajax
@login_required
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
		return HttpResponseRedirect(reverse('reviews.views.list_details', kwargs={'feedback_id':feedback_id}))
		# return HttpResponse(json.dumps({
		# 	'id': d.id,
		# 	'date_written': d.date_written,
		# 	'written_by': request.user.full_name,
		# 	'body': d.body,
		# }, cls=DjangoJSONEncoder))

def list_details(request, feedback_id):
	page = request.GET.get('page')
	if not page:
		page = 1
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

def search_feedback(request):
	if request.method == 'GET' and request.GET:
		query = request.GET.get('query', None)
		item_id = request.GET.get('item_id', None)
		is_positive = request.GET.get('is_positive', None)
		if query and item_id and is_positive != None:
			query = query.strip()
			query = " | ".join(query.split(' '))
			print query
			connection = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
			with closing(connection.cursor()) as cursor:
				cursor.execute("select * from reviews_feedback where match('@body {0}') and item_id={1} and is_positive={2} OPTION ranker=matchany".format(query, int(item_id), int(is_positive))) # is it safe?
				ids = [row[0] for row in cursor.fetchall()] # is it efficient?
			connection.close()
			feedbacks = Feedback.objects.filter(id__in=ids).extra(
				select={'manual': 'FIELD(id, %s)' % ','.join(map(str, ids))},
				order_by=['manual']
				)
			result = []
			for feedback in feedbacks:
				result.append({'id': feedback.id, 'body': feedback.body})
			return HttpResponse(json.dumps(result))
		else:
			return HttpResponse(json.dumps(""))
	else:
		raise Http404

@require_POST
@login_required_ajax
def set_priority(request, feedback_id):
	value = request.POST.get('value', None)
	if not value:
		raise HttpResponseBadRequest(json.dumps({'message': 'Not enough arguments'}))

	try:
		priority = Priority(
			feedback=Feedback(id=feedback_id),
			value=int(value)
		)
		priority.save(request=request)
	except Exception as e:
		return HttpResponseBadRequest(json.dumps({'message': e.value}))

	return HttpResponse(1)

@require_POST
@login_required_ajax
def unset_priority(request, feedback_id):
	value = request.POST.get('value', None)
	if not value:
		raise HttpResponseBadRequest(json.dumps({'message': 'Not enough arguments'}))
	
	try:
		Priority.objects.get(feedback_id=feedback_id, marked_by=request.user.id, value=value).delete(request=request)
	except Priority.DoesNotExist:
		return HttpResponseBadRequest(json.dumps({'message': 'No such Priority'}))
	except Exception as e:
		return HttpResponseBadRequest(json.dumps({'message': e.value}))

	return HttpResponse(1)

@login_required_ajax
@require_POST
def suggest_edit(request, feedback_id):
	form = FeedbackSuggestEditForm(request.POST)
	if form.is_valid():
		feedback = get_object_or_404(Feedback, pk=feedback_id)
		suggestion = FeedbackEditSuggestion(feedback=feedback,
			suggested_value=form.cleaned_data.get('suggested_value'),
			suggested_by_id=request.user.id,
			date_suggested=timezone.now())
		try:
			suggestion.full_clean()
			suggestion.save()
		except ValidationError as e:
			return HttpResponseBadRequest(json.dumps(e.message_dict))
		return HttpResponse(1);
	else:
		return HttpResponseBadRequest(json.dumps(form.errors))

@require_GET
@permission_required('reviews.moderate_feedback')
def moderate_feedback(request):
	pass

@permission_required('reviews.moderate_feedback')
def edit_feedback(request, feedback_id):
	feedback = get_object_or_404(Feedback, pk=feedback_id)
	if request.method == 'POST':
		form = FeedbackEditForm(request.POST)
		if form.is_valid():
			old_value = feedback.__unicode__()
			feedback.body = form.cleaned_data.get('body', feedback.body)
			try:
				feedback.full_clean()
				feedback.save()
			except ValidationError as e:
				return HttpResponseBadRequest(json.dumps(e.message_dict))
			# create history_log
			history_log = FeedbackEditHistory(feedback=feedback,
				edited_by_id=request.user.id,
				date_edited=timezone.now(),
				old_value=old_value)
			history_log.save()

			return HttpResponseRedirect(reverse('items.views.view', kwargs={'item_id': feedback.item_id}))
	else:
		form = FeedbackEditForm(initial={'body': feedback.body})
	
	return render(request, 'reviews/feedbacks/edit_feedback.html', {
			'form': form,
			'feedback': feedback,
			})

@permission_required('reviews.moderate_feedback')
def moderate_feedback(request):
	suggestions = FeedbackEditSuggestion.objects.filter(is_resolved=False).prefetch_related('feedback').order_by('-date_suggested')
	return render(request, 'reviews/feedbacks/moderate_feedback.html', {
		'suggestions': suggestions,
		})

@require_POST
@permission_required('reviews.moderate_feedback')
def accept_feedbackeditsuggestion(request, suggestion_id):
	suggestion = get_object_or_404(FeedbackEditSuggestion, pk=suggestion_id)
	feedback = suggestion.feedback
	old_value = feedback.body
	feedback.body = suggestion.suggested_value
	try:
		feedback.full_clean()
		feedback.save()
	except ValidationError as e:
		HttpResponseBadRequest(json.dumps(e.message_dict))

	history_log = FeedbackEditHistory(feedback=feedback,
				edited_by_id=request.user.id,
				date_edited=timezone.now(),
				old_value=old_value)
	history_log.save()
	
	suggestion.is_resolved = True
	suggestion.resolved_by = request.user
	suggestion.save()
	return HttpResponse(1)

@require_POST
@permission_required('reviews.moderate_feedback')
def ignore_feedbackeditsuggestion(request, suggestion_id):
	suggestion = get_object_or_404(FeedbackEditSuggestion, pk=suggestion_id)
	suggestion.is_resolved = True
	suggestion.resolved_by = request.user
	suggestion.save()
	return HttpResponse(1)