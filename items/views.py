from django.template import RequestContext, loader
from items.models import Item, ItemAddForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

def index(request):
	latest_item_list = Item.objects.all().order_by('-date_created')[:5]
	t = loader.get_template('items/index.html')
	rc = RequestContext(request, {
		'latest_item_list': latest_item_list,
	})
	return HttpResponse(t.render(rc))

def add(request):
	if request.method == 'POST':
		form = ItemAddForm(request.POST)
		if form.is_valid():
			i = Item(
				name=form.cleaned_data['name'],
				date_created=form.cleaned_data['date_created'],
				created_by=form.cleaned_data['created_by'],
				category=form.cleaned_data['category']
			)
			# i = Item(**form.cleaned_data)
			i.save()
			return HttpResponseRedirect(reverse('items.views.index'))
	else:
		form = ItemAddForm() # An unbound form

	return render(request, 'items/add.html', {
		'form': form,
	})