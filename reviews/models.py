from django.db import models
from django.conf import settings
from items.models import Item, ItemUsageExperience
from django.forms import ModelForm
from django.db.models.signals import post_save, pre_delete, post_delete
from reviews.vote_type_utils import get_vt_weight
from django.dispatch import receiver
from django.db.models import F
from reviews.sphinxql import sphinxql_query
from reviews.custom_exceptions import UserDidNotUseItem, PriorityOutOfRange, MustAgreeFirst, WrongOrderPriority
from customauth.models import CustomUser
from django.utils import timezone

# Create your models here.
# pragmatique

class Feedback(models.Model):
	body = models.CharField(max_length=144)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_created = models.DateTimeField('date created')
	item = models.ForeignKey(Item)
	is_positive = models.BooleanField(default=True)
	score = models.IntegerField(default=0)
	is_active = models.BooleanField(default=True)
	date_edited = models.DateTimeField('date last edited', null=True, blank=True)
	
	agrees_count = models.PositiveIntegerField(default=0)
	disagrees_count = models.PositiveIntegerField(default=0)
	
	details_count = models.PositiveIntegerField(default=0)

	priority_1_count = models.PositiveIntegerField(default=0)
	priority_2_count = models.PositiveIntegerField(default=0)
	priority_3_count = models.PositiveIntegerField(default=0)

	class Meta:
		unique_together = ('body', 'item', 'is_positive')
		ordering = ('-score', 'date_created')

	def save(self, request=None, *args, **kwargs):
		if request:	# if this is view call
			try:
				experience = ItemUsageExperience.objects.get(user_id=request.user.id, item_id=self.item_id)
			except ItemUsageExperience.DoesNotExist:
				raise UserDidNotUseItem
		super(Feedback, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.body

@receiver(post_save, sender=Feedback)
def feedback_sphinx_save(sender, instance, created, **kwargs):
	if created:
		q = "insert into reviews_feedback values({0}, '{1}', {2}, {3}, {4})".format(instance.id, instance.body, instance.created_by_id, int(instance.is_positive), int(instance.item_id))
		rows_affected = sphinxql_query(q)
		assert rows_affected > 0

@receiver(pre_delete, sender=Feedback)
def feedback_sphinx_delete(sender, instance, **kwargs):
	q = "delete from reviews_feedback where id={0}".format(instance.id)
	sphinxql_query(q)

class ModerationReason(models.Model):
	reason = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.reason

class FeedbackCloseInfo(models.Model):
	feedback = models.ForeignKey(Feedback)
	closed_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_closed = models.DateTimeField('date closed')
	reason = models.ForeignKey(ModerationReason)

	def __unicode__(self):
		return self.feedback + self.reason

class FeedbackEditInfo(models.Model):
	feedback = models.ForeignKey(Feedback)
	edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_edited = models.DateTimeField('date closed')
	old_value = models.CharField(max_length=144)
	
	def __unicode__(self):
		return self.feedback + self.old_value

class VoteType(models.Model):
	name = models.CharField(max_length=32, unique=True)
	weight = models.IntegerField()

	def __unicode__(self):
		return self.name

class Vote(models.Model):
	feedback = models.ForeignKey(Feedback)
	voted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	type = models.ForeignKey(VoteType)
	date_voted = models.DateTimeField('date voted')

	def __unicode__(self):
		return self.type.name

	def save(self, request=None, *args, **kwargs):
		if not self.id:
			feedback = Feedback.objects.get(pk=self.feedback_id)

			if request:	# if this is view call
				try:
					experience = ItemUsageExperience.objects.get(user_id=request.user.id, item_id=feedback.item_id)
				except ItemUsageExperience.DoesNotExist:
					raise UserDidNotUseItem
		super(Vote, self).save(*args, **kwargs)

	class Meta:
		unique_together = ('feedback', 'voted_by')

@receiver(post_save, sender=Vote)
def vote_post_save(sender, instance, created, **kwargs):
	if created:
		Feedback.objects.filter(id=instance.feedback_id).update(score=F('score') + get_vt_weight(int(instance.type_id)))

		if int(instance.type_id) == 1:	# Agree
			Feedback.objects.filter(id=instance.feedback_id).update(agrees_count=F('agrees_count') + 1)
		elif int(instance.type_id) == 2:	# Disagree
			Feedback.objects.filter(id=instance.feedback_id).update(disagrees_count=F('disagrees_count') + 1)

@receiver(post_delete, sender=Vote)
def vote_post_delete(sender, instance, **kwargs):
	Feedback.objects.filter(id=instance.feedback_id).update(score=F('score') - get_vt_weight(int(instance.type_id)))

	if int(instance.type_id) == 1:	# vote.type_id = 1 is Agree
		Feedback.objects.filter(id=instance.feedback_id).update(agrees_count=F('agrees_count') - 1)
	elif int(instance.type_id) == 2:	# Disagree
		Feedback.objects.filter(id=instance.feedback_id).update(disagrees_count=F('disagrees_count') - 1)

	if instance.type_id == 1:	# 1 = Agree
		try:
			priority = Priority.objects.get(marked_by_id=instance.voted_by_id, feedback_id=instance.feedback_id)
		except Priority.DoesNotExist:
			pass
		else:
			feedback = Feedback.objects.get(pk=priority.feedback_id)
			priorities = Priority.objects.filter(marked_by_id=instance.voted_by_id, feedback__item=feedback.item_id, feedback__is_positive=feedback.is_positive, value__gte=priority.value)
			for priority in priorities:
				priority.delete()

class Detail(models.Model):
	body = models.TextField()
	feedback = models.ForeignKey(Feedback)
	written_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_written = models.DateTimeField('date created')

	class Meta:
		ordering = ('-date_written',)

	def save(self, request=None, *args, **kwargs):
		if request:	# if this is view call
			feedback = Feedback.objects.get(pk=self.feedback_id)
			try:
				experience = ItemUsageExperience.objects.get(user_id=request.user.id, item_id=feedback.item_id)
			except ItemUsageExperience.DoesNotExist:
				raise UserDidNotUseItem
		super(Detail, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.body[:20] + "..."

@receiver(post_save, sender=Detail)
def detail_post_save(sender, instance, created, **kwargs):
	if created:
		Feedback.objects.filter(id=instance.feedback_id).update(details_count=F('details_count') + 1)

@receiver(post_delete, sender=Detail)
def detail_post_delete(sender, instance, **kwargs):
	Feedback.objects.filter(id=instance.feedback_id).update(details_count=F('details_count') - 1)

class DetailAddForm(ModelForm):
	class Meta:
		model = Detail
		fields = ('body', )

class Priority(models.Model):
	feedback = models.ForeignKey(Feedback)
	marked_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	value = models.PositiveSmallIntegerField()
	date_marked = models.DateTimeField(default=timezone.now)

	VALUE_RANGE = (1, 3)

	def save(self, request=None, *args, **kwargs):
		if request:
			agree_votetype_id = 1
			
			try:
				vote = Vote.objects.get(voted_by=request.user.id, feedback_id=self.feedback_id, type_id=agree_votetype_id)
			except Vote.DoesNotExist:
				raise MustAgreeFirst

			if self.value < self.VALUE_RANGE[0] or self.value > self.VALUE_RANGE[1]:
				raise PriorityOutOfRange
			
			feedback = Feedback.objects.get(pk=self.feedback_id)
			priorities_num = Priority.objects.filter(feedback__item=feedback.item_id, feedback__is_positive=feedback.is_positive, marked_by=request.user.id).count()
			if priorities_num + 1 != self.value:
				raise WrongOrderPriority
			
			# auto set
			self.marked_by = CustomUser(id=request.user.id)
					

		super(Priority, self).save(*args, **kwargs)

	def delete(self, request=None, *args, **kwargs):
		if request:
			feedback = Feedback.objects.get(pk=self.feedback_id)
			priorities_num = Priority.objects.filter(feedback__item=feedback.item_id, feedback__is_positive=feedback.is_positive, marked_by=request.user.id).count()
			if priorities_num != self.value:
				raise WrongOrderPriority

		super(Priority, self).delete(*args, **kwargs)

	class Meta:
		unique_together = ('feedback', 'marked_by')

@receiver(post_save, sender=Priority)
def priority_post_save(sender, instance, created, **kwargs):
	if created:
		if int(instance.value) == 1:
			Feedback.objects.filter(id=instance.feedback_id).update(priority_1_count=F('priority_1_count') + 1)
		elif int(instance.value) == 2:
			Feedback.objects.filter(id=instance.feedback_id).update(priority_2_count=F('priority_2_count') + 1)
		elif int(instance.value) == 3:
			Feedback.objects.filter(id=instance.feedback_id).update(priority_3_count=F('priority_3_count') + 1)

@receiver(post_delete, sender=Priority)
def priority_post_delete(sender, instance, **kwargs):
	if int(instance.value) == 1:
		Feedback.objects.filter(id=instance.feedback_id).update(priority_1_count=F('priority_1_count') - 1)
	elif int(instance.value) == 2:
		Feedback.objects.filter(id=instance.feedback_id).update(priority_2_count=F('priority_2_count') - 1)
	elif int(instance.value) == 3:
		Feedback.objects.filter(id=instance.feedback_id).update(priority_3_count=F('priority_3_count') - 1)