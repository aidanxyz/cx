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
from django.core import serializers
from django.conf import settings
import MySQLdb
import json

def index(request):
	latest_item_list = Item.objects.all().order_by('-date_created')[:5]
	t = loader.get_template('items/index.html')
	rc = RequestContext(request, {
		'latest_item_list': latest_item_list,
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
			return HttpResponseRedirect(reverse('items.views.index'))
	else:
		form = ItemAddForm() # An unbound form

	return render(request, 'items/add.html', {
		'form': form,
	})

def search(request):
	if request.method == 'GET' and request.GET:
		q = str(request.GET['query'])
		if q != "":
			db = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
			cursor = db.cursor()
			cursor.execute("select * from items_item where match('%s')" % q) # is it safe?
			ids = tuple(row[0] for row in cursor.fetchall()) # is it efficient?
			items = Item.objects.filter(id__in=ids)
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

	item_used_by_user = False
	add_select = {
		'num_agrees': 'select count(*) from reviews_vote where reviews_vote.type_id=1 and reviews_vote.feedback_id = reviews_feedback.id',
		'num_disagrees': 'select count(*) from reviews_vote where reviews_vote.type_id=2 and reviews_vote.feedback_id = reviews_feedback.id',
		'num_details': 'select count(*) from reviews_detail where reviews_feedback.id = reviews_detail.feedback_id'
	}
	if request.user.is_authenticated():
		add_select['vote_type_id'] = 'select type_id from reviews_vote where reviews_vote.feedback_id=reviews_feedback.id and reviews_vote.voted_by_id=%s' % (request.user.id)
		if request.user.items_used.filter(id=item_id):
			item_used_by_user = True

	feedbacks = item.feedback_set.filter(is_active=True).extra(select=add_select)
	return render(request, 'items/view.html', {
		'item': item,
		'feedbacks': feedbacks,
		'item_used_by_user': item_used_by_user,
	})

@login_required_ajax
@require_POST
def add_item_to_users_items_list(request, item_id):
	try:
		item = Item.objects.get(pk=item_id)
	except Item.DoesNotExist:
		raise Http404
	request.user.items_used.add(item)
	return HttpResponse(json.dumps({'success': True, 'message': 'added'}))