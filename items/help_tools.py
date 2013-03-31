from items.models import ItemUsageExperience
from reviews.custom_exceptions import UserDidNotUseItem

def assert_user_used_item(user_id, item_id):
	try:
		experience = ItemUsageExperience.objects.get(user_id=user_id, item_id=item_id)
	except ItemUsageExperience.DoesNotExist:
		raise UserDidNotUseItem