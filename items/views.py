from django.template import RequestContext, loader
from items.models import Item, ItemAddForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from customauth.decorators import login_required_ajax, permission_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from customauth.models import CustomUser
from items.models import *
from django.core import serializers
from django.conf import settings
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count
from django.core.serializers.json import DjangoJSONEncoder

def home(request):
	return render(request, 'home.html', {})

def get_latest(request, number):
	number = int(number)
	if 0 < number < 10:
		items = Item.objects.filter(is_active=True).order_by('-date_created')[:number]
		results = []
		for item in items:
			results.append({'id': item.id, 'name': item.name})
		return HttpResponse(json.dumps(results))
	else:
		return HttpResponseBadRequest('yupi')

def explore(request):
	category_name = request.GET.get('category', 'all')
	if category_name == 'all':
		latest_items_list = Item.objects.filter(is_active=True).prefetch_related('latest_feedback').order_by('-date_created')
	else:
		category = get_object_or_404(Category, name=category_name)
		latest_items_list = Item.objects.filter(is_active=True, category_id=category.id).prefetch_related('latest_feedback').order_by('-date_created')

	t = loader.get_template('items/explore.html')
	rc = RequestContext(request, {
		'latest_item_list': latest_items_list, 
		'category_name': category_name,
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
			duplicates_list = i.get_similar_item_ids()
			if len(duplicates_list) > 0:
				possible_duplicates = ItemPossibleDuplicates(str_list=str(duplicates_list), number=len(duplicates_list))
				possible_duplicates.save()
				i.possible_duplicates = possible_duplicates
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
			i = Item()
			ids = i.get_similar_item_ids(name=query)
			items = Item.objects.filter(id__in=ids, is_active=True).extra(
				select={'manual': 'FIELD(id, %s)' % ','.join(map(str, ids))},
				order_by=['manual']
				)
			results = []
			for item in items:
				results.append({'id': item.id, 'name': item.name})
			return HttpResponse(json.dumps(results))
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
	try:
		latest_price = Price.objects.filter(item_id=item_id, is_approved=True).latest('date_added')
	except Price.DoesNotExist:
		latest_price = None

	context = {
		'item': item,
		'feedbacks': feedbacks,
		'experience': experience,
		'latest_price': latest_price,
	}
	if not experience:
		context['usage_form'] = ItemUsageForm()
	return render(request, 'items/view.html', context)

@login_required_ajax
@require_POST
def add_usage_experience(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	experience = ItemUsageExperience(user=request.user, 
		item=item, 
		duration=ItemUsageDurationType(id=request.POST.get('duration')), 
		rating=ItemUsageRatingType(id=request.POST.get('rating')),
		date_verified=timezone.now()
	)
	try:
		experience.full_clean()
		experience.save()

		item.avg_rating = ItemUsageExperience.objects.filter(item=item).aggregate(Avg('rating__value'))['rating__value__avg']
		item.reviewers_count = item.reviewers_count + 1
		item.save()
	except ValidationError as e:
		return HttpResponseBadRequest(json.dumps(e.message_dict))
	
	return HttpResponse(json.dumps({
		'avg_rating': item.avg_rating,
		'item_id': item.id,
		'user_rating': ItemUsageRatingType.objects.get(pk=experience.rating_id).value,
		'reviewers_count': item.reviewers_count,
		}))

	# return HttpResponse(json.dumps({
	# 	'date_verified': experience.date_verified
	# }, cls=DjangoJSONEncoder))

@login_required
@permission_required('items.moderate_items')
def add_item_image(request, item_id):
	if request.method == 'POST':
		form = ItemImageUploadForm(request.POST, request.FILES)
		if form.is_valid() and form.clean_image_size():
			item_image = ItemImage(
				item=Item(id=item_id),
				image=request.FILES['image'],
				uploaded_by=request.user,
				date_uploaded=timezone.now())
			item_image.save()
			return HttpResponseRedirect('/items/' + item_id + '/gallery/')
	else:
		form = ItemImageUploadForm()

	return render(request, 'items/item_images/add.html', {
		'form': form, 
		'item_id': item_id,
	})

def view_item_images(request, item_id):
	if request.method == 'GET':
		try:
			item = Item.objects.get(pk=item_id)
		except Item.DoesNotExist:
			return Http404()

		item_images = ItemImage.objects.filter(item_id=item_id)

		return render(request, 'items/item_images/view.html', {
			'item': item,
			'item_images': item_images,
		})
	else:
		return HttpResponseBadRequest()

@login_required
@permission_required('items.moderate_items')
def moderate_items(request):
	items = Item.objects.filter(is_approved=False, is_active=True).order_by('-date_created').prefetch_related('possible_duplicates')
	return render(request, 'items/moderation/moderate_items.html', {
		'items': items,
	})

@require_POST
@permission_required('items.moderate_items')
def set_cover_image(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	image = get_object_or_404(ItemImage, pk=request.POST.get('image_id', None))
	if image.item != item:
		return HttpResponseBadRequest(json.dumps({'message': 'Image does not belong to this item'}))
	item.cover_image = image
	item.save()
	return HttpResponse(1)

@require_POST
@login_required
@permission_required('items.moderate_items')
def approve_item(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	if not item.is_active:
		history_log = ItemDeactivationHistory.objects.filter(item=item).latest('date_disactivated')
		return HttpResponseBadRequest(json.dumps({
			'status': 'deactivated',
			'moderated_by': history_log.moderator.full_name,
			}))

	if not item.is_approved:
		item.is_approved = True
		item.save()
		history_log = ItemApprovalHistory(item=item, 
			moderator_id=request.user.id, 
			date_approved=timezone.now())
		history_log.save()

		return HttpResponse(json.dumps({
			'status': 'approved', 
			}))
	else:
		history_log = ItemApprovalHistory.objects.filter(item=item).latest('date_approved')
		return HttpResponseBadRequest(json.dumps({
			'status': 'approved',
			'moderated_by': history_log.moderator.full_name,
			}))

@require_POST
@login_required
@permission_required('items.moderate_items')
def deactivate_item(request, item_id):
	form = ItemDeactivationForm(request.POST)
	if form.is_valid():	
		reason = form.cleaned_data.get('reason')
		duplicate_of = form.cleaned_data.get('duplicate_of', None)
		
		if reason.id == 1 and not duplicate_of: # 1 is duplicate
			return HttpResponseBadRequest(json.dumps({'message': 'No duplicate is provided'}))

		item = get_object_or_404(Item, pk=item_id)
		if not item.is_active:
			return HttpResponseBadRequest(json.dumps({'message': 'Was already deactivated'}))
		item.is_active = False
		item.save()
		history_log = ItemDeactivationHistory(item=item, 
			moderator_id=request.user.id, 
			date_deactivated=timezone.now(),
			reason=reason,
			duplicate_of=duplicate_of)
		try:
			history_log.full_clean()
			history_log.save()
		except ValidationError as e:
			return HttpResponseBadRequest(json.dumps(e.message_dict))
		
		return HttpResponse(json.dumps({'item_id': item.id}))			
	else:
		return HttpResponseBadRequest(json.dumps(form.errors))

@login_required
@permission_required('items.moderate_items')
def edit_item(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	if request.method == 'POST':
		form = ItemEditForm(request.POST)
		if form.is_valid():
			old_value = item.__unicode__()
			item.name = form.cleaned_data.get('name', item.name)
			item.category = form.cleaned_data.get('category', item.category)
			try:
				item.full_clean()
				item.save()
			except ValidationError as e:
				return HttpResponseBadRequest(json.dumps(e.message_dict))
			history_log = ItemEditHistory(item=item,
				moderator_id=request.user.id,
				date_edited=timezone.now(),
				reason=form.cleaned_data.get('reason'),
				other_reason=form.cleaned_data.get('other_reason', None),
				old_value=old_value)
			try:
				history_log.full_clean()
				history_log.save()
			except ValidationError as e:
				return HttpResponseBadRequest(json.dumps(e.message_dict))

			return HttpResponseRedirect(reverse('items.views.moderate_items'))
	else:
		form = ItemEditForm(initial={'name': item.name, 'category': item.category})
	
	return render(request, 'items/moderation/edit_item.html', {
			'form': form,
			'item': item,
			})

@require_POST
@login_required_ajax
@permission_required('items.moderate_items')
def get_possible_duplicates(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	possible_duplicates = item.possible_duplicates
	if possible_duplicates and possible_duplicates.number > 0:
		items = Item.objects.filter(id__in=eval(possible_duplicates.str_list))
		d = {}
		for item in items:
			d[item.id] = item.name
		return HttpResponse(json.dumps(d))
	else:
		return HttpResponseBadRequest(json.dumps({'message': 'Ops, no duplicates now!'}))

@login_required
def add_price(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	if request.method == 'POST':
		form = PriceAddForm(request.POST)
		if form.is_valid():
			price = Price(item=item, 
				value=form.cleaned_data.get('value'),
				source_url=form.cleaned_data.get('source_url'),
				date_added=timezone.now(),
				added_by=request.user)
			price.save()

			return HttpResponseRedirect(reverse('items.views.view', kwargs={'item_id': item_id}))
	else:
		form = PriceAddForm()

	return render(request, 'items/moderation/add_price.html', {
		'item': item,
		'form': form, 
		})

@permission_required('items.moderate_items')
def moderate_prices(request):
	prices = Price.objects.filter(is_approved=False, is_active=True).order_by('-date_added')
	return render(request, 'items/moderation/moderate_prices.html', {
		'prices': prices,
		})

@require_POST
@permission_required('items.moderate_items')
def approve_price(request, price_id):
	price = get_object_or_404(Price, pk=price_id)
	price.is_approved = True
	price.resolved_by = request.user
	price.save()
	item = price.item
	item.latest_price = price.value
	item.save()
	return HttpResponse(1)

@require_POST
@permission_required('items.moderate_items')
def ignore_price(request, price_id):
	price = get_object_or_404(Price, pk=price_id)
	price.is_active = False
	price.resolved_by = request.user
	price.save()
	return HttpResponse(1)

@login_required_ajax
@permission_required('items.moderate_items')
def get_stats(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	
	prices = item.price_set.order_by('date_added')
	prices_table = []
	for price in prices:
		prices_table.append([price.date_added, price.value, 'S', price.source_url])
	
	ratings = ItemUsageExperience.objects.filter(item_id=item_id).values('rating_id').annotate(total=Count('id'))
	print ratings
	ratings_map = {1: 'Terrible', 2: 'Bad', 3: 'Normal', 4: 'Good', 5: 'Excellent'}
	ratings_table = [['Rating name', 'Number of people']]
	for d in ratings:
		ratings_table.append([ratings_map[int(d['rating_id'])], int(d['total'])])

	years = ItemUsageExperience.objects.filter(item_id=1).values('user__year_of_birth').annotate(total=Count('id'))
	ages_table = [['Age', 'Number of people'], ['N<20', 0], ['20<N<30', 0], ['30<N<50', 0], ['N>60', 0]]
	for d in years:
		age = timezone.now().year - int(d['user__year_of_birth'])
		if age < 20:
			ages_table[1][1] += int(d['total'])
		elif age < 30:
			ages_table[2][1] += int(d['total'])
		elif age < 50:
			ages_table[3][1] += int(d['total'])
		elif age > 60:
			ages_table[4][1] += int(d['total'])

	countries = ItemUsageExperience.objects.filter(item_id=1).values('user__country__name').annotate(total=Count('id'))
	countries_table = [['Country name', 'Number of people']]
	for d in countries:
		countries_table.append([d['user__country__name'], int(d['total'])])

	genders = ItemUsageExperience.objects.filter(item_id=1).values('user__gender').annotate(total=Count('id'))
	genders_table = [['Gender', 'Number of people']]
	for d in genders:
		genders_table.append([d['user__gender'], int(d['total'])])


	return HttpResponse(json.dumps({
			'ratings_table': ratings_table,
			'ages_table': ages_table,
			'countries_table': countries_table,
			'genders_table': genders_table,
			'prices_table': prices_table,
		}, cls=DjangoJSONEncoder))

@login_required
@permission_required('items.moderate_items')
def stats_page(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	return render(request, 'items/stats.html', {
		'item': item,
		});
