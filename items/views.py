from django.template import RequestContext, loader
from items.models import Item, ItemAddForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from customauth.models import CustomUser
from django.core import serializers
from django.conf import settings
import MySQLdb

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
			# ...now save to Sphinx
			db = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
			cursor = db.cursor()
			rows_affected = cursor.execute("insert into items_item values({0}, '{1}', {2}, {3})".format(i.id, i.name, request.user.id, i.category_id)) 
			assert rows_affected > 0

			return HttpResponseRedirect(reverse('items.views.index'))
	else:
		form = ItemAddForm() # An unbound form

	return render(request, 'items/add.html', {
		'form': form,
	})

def search(request):
	if request.method == 'GET' and request.GET:
		t = str(request.GET['text'])
		if t != "":
			db = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
			cursor = db.cursor()
			cursor.execute("select * from items_item where match('%s')" % t) # is it safe?
			ids = tuple(row[0] for row in cursor.fetchall()) # is it efficient?
			items = Item.objects.filter(id__in=ids)
			return HttpResponse(serializers.serialize('json', items))
		else:
			return HttpResponse(serializers.serialize('json', ""))
	else:
		raise Http404