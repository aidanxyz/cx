from reviews.sphinxql import sphinxql_query
from django.db.models import F

def feedback_sphinx_save(sender, instance, created, **kwargs):
	if created:
		q = "insert into reviews_feedback values({0}, '{1}', {2}, {3})".format(instance.id, instance.body, instance.created_by_id, int(instance.is_positive))
		rows_affected = sphinxql_query(q)
		assert rows_affected > 0

def feedback_sphinx_delete(sender, instance, **kwargs):
	q = "delete from reviews_feedback where id={0}".format(instance.id)
	sphinxql_query(q)

def vote_save_score(sender, instance, created, **kwargs):
	if created: # instance is Vote object
		instance.feedback.score = F('score') + vote_type_weight(instance.type_id)
		instance.feedback.save()

def vote_delete_score(sender, instance, **kwargs):
	# instance is Vote object
	instance.feedback.score = F('score') - vote_type_weight(instance.type_id)
	instance.feedback.save()

def vote_type_weight(id):
	types = {
		1: 1,
		2: -1
	}
	return types[id]