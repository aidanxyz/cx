from django.db import models
from django.conf import settings
from items.models import Item
from django.forms import ModelForm
from django.db.models.signals import post_save, pre_delete
from reviews.receivers import feedback_sphinx_save, feedback_sphinx_delete

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

	class Meta:
		unique_together = ('body', 'item', 'is_positive')
		ordering = ('score',)

	def __unicode__(self):
		return self.body

# connect signals to receiver/handlers
post_save.connect(feedback_sphinx_save, sender=Feedback)
pre_delete.connect(feedback_sphinx_delete, sender=Feedback)

class PositiveFeedbackAddForm(ModelForm):
	class Meta:
		model = Feedback
		fields = ('body',)

class NegativeFeedbackAddForm(ModelForm):
	class Meta:
		model = Feedback
		fields = ('body',)

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

	class Meta:
		unique_together = ('feedback', 'voted_by')