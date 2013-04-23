from django.template import RequestContext, loader
from items.models import Item, ItemAddForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from customauth.decorators import login_required_ajax
from django.views.decorators.http import require_POST
from django.utils import timezone
from customauth.models import CustomUser
from items.models import ItemUsageExperience, ItemUsageForm, ItemUsageDurationType, ItemUsageRatingType
from django.core import serializers
from django.conf import settings
import MySQLdb
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Q

def index(request):
	latest_items_list = Item.objects.filter(Q(status='C') | Q(status='NC')).prefetch_related('latest_feedback')

	t = loader.get_template('items/index.html')
	rc = RequestContext(request, {
		'latest_item_list': latest_items_list,
	})
	return HttpResponse(t.render(rc))

@login_required
def add(request):
	if request.method == 'POST':
		form = ItemAddForm(request.POST)
		if form.is_valid():
			# i = Item(**form.cleaned_data)
			i = Item(
				name=form.cleaned_data['name'],
				date_created=timezone.now(),
				created_by=CustomUser(id=request.user.id),
				category=form.cleaned_data['category']
			)
			i.save()
			return HttpResponseRedirect(reverse('items.views.view', kwargs={'item_id': i.id}))
	else:
		form = ItemAddForm() # An unbound form

	return render(request, 'items/add.html', {
		'form': form,
	})

def search(request):
	if request.method == 'GET' and request.GET:
		query = request.GET.get('query', None)
		if query:
			db = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
			cursor = db.cursor()
			cursor.execute("select * from items_item where match('@name %s')" % str(query)) # is it safe?
			ids = tuple(row[0] for row in cursor.fetchall()) # is it efficient?
			items = Item.objects.filter(id__in=ids).extra(
				select={'manual': 'FIELD(id, %s)' % ','.join(map(str, ids))},
				order_by=['manual']
				)
			result = []
			for item in items:
				result.append({'id': item.id, 'name': item.name})
			return HttpResponse(json.dumps(result))
		else:
			return HttpResponse(json.dumps(""))
	else:
		raise Http404

def view(request, item_id):
	try:
		item = Item.objects.get(pk=item_id)
	except Item.DoesNotExist:
		raise Http404
	else:
		Item.objects.filter(pk=item_id).update(views_count = F('views_count') + 1)

	experience = None
	add_select = {}
	if request.user.is_authenticated():
		# votes by user
		add_select['voted_type_id'] = 'select type_id from reviews_vote where reviews_vote.feedback_id=reviews_feedback.id and reviews_vote.voted_by_id=%s' % (request.user.id)
		# priorities set by user
		add_select['priority_value'] = 'select value from reviews_priority where reviews_priority.feedback_id=reviews_feedback.id and reviews_priority.marked_by_id=%s' % (request.user.id)
		try:
			experience = ItemUsageExperience.objects.get(user=request.user, item=item)
		except ItemUsageExperience.DoesNotExist:
			experience = None

	feedbacks = item.feedback_set.filter(is_active=True).extra(select=add_select)
	context = {
		'item': item,
		'feedbacks': feedbacks,
		'experience': experience,
	}
	if not experience:
		context['usage_form'] = ItemUsageForm()
	return render(request, 'items/view.html', context)

@login_required_ajax
@require_POST
def add_usage_experience(request, item_id):
	try:
		item = Item.objects.get(pk=item_id)
	except Item.DoesNotExist:
		raise Http404
	experience = ItemUsageExperience(user=request.user, 
		item=item, 
		duration=ItemUsageDurationType(id=request.POST.get('duration')), 
		rating=ItemUsageRatingType(id=request.POST.get('rating')),
		date_verified=timezone.now()
	)
	try:
		experience.full_clean()
		experience.save()
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	return HttpResponse(json.dumps({
		'date_verified': experience.date_verified
	}, cls=DjangoJSONEncoder))