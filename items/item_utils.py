def assert_user_used_item(user_id, item_id):
	from items.models import ItemUsageExperience
	from reviews.custom_exceptions import UserDidNotUseItem
	try:
		experience = ItemUsageExperience.objects.get(user_id=user_id, item_id=item_id)
	except ItemUsageExperience.DoesNotExist:
		raise UserDidNotUseItem

def get_item_image_path(instance, filename):
	import os, uuid
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('itemimage_origs', filename)