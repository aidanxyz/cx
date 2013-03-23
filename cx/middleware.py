from items.models import Item
from django.http import Http404

class IdToObjectMiddleware():
	def process_view(self, request, view_func, view_args, view_kwargs):
		if 'item' in view_kwargs:
			try:
				view_kwargs['item'] = Item.objects.get(pk=view_kwargs['item'])
			except Item.DoesNotExist:
				raise Http404