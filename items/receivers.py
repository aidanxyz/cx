from reviews.sphinxql import sphinxql_query

def save_item_sphinx(sender, instance, created, **kwargs):
	if created:
		q = "insert into items_item values({0}, '{1}', {2}, {3})".format(instance.id, instance.name, instance.created_by_id, instance.category_id)
		assert sphinxql_query(q) > 0

def delete_item_sphinx(sender, instance, **kwargs):
	q = "delete from items_item where id={0}".format(instance.id)
	sphinxql_query(q)