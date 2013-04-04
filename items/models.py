from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db.models.signals import post_save, pre_delete
from items.receivers import save_item_sphinx, delete_item_sphinx

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=200, unique=True)
	date_created = models.DateTimeField('date created')
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	category = models.ForeignKey(Category)
	STATUS_CHOICES = (
		('NC', 'Not checked'),
		('C', 'Checked'),
		('NA', 'Not active')
	)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NC')
	
	def __unicode__(self):
		return self.name

class ItemAddForm(ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'category')

post_save.connect(save_item_sphinx, sender=Item)
pre_delete.connect(delete_item_sphinx, sender=Item)

class ItemUsageDurationType(models.Model):
	string = models.CharField(max_length=255)
	value = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ('string', 'value')

	def __unicode__(self):
		return self.string

class ItemUsageRatingType(models.Model):
	string = models.CharField(max_length=64)
	value = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ('string', 'value')

	def __unicode__(self):
		return self.string

class ItemUsageExperience(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	item = models.ForeignKey(Item)
	duration = models.ForeignKey(ItemUsageDurationType, default=1)
	rating = models.ForeignKey(ItemUsageRatingType, default=4)
	date_verified = models.DateTimeField('date when user verified usage')

class ItemUsageForm(ModelForm):
	class Meta:
		model = ItemUsageExperience
		fields = ('duration', 'rating')
