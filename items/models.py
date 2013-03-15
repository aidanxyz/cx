from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db.models.signals import post_save, pre_delete
from items.receivers import save_item_sphinx, delete_item_sphinx
from customauth.models import CustomUser

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
	
	def __unicode__(self):
		return self.name

class ItemAddForm(ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'category')

class UsageExperience(models.Model):
	LESS_THAN_MONTH = 20
	MORE_THAN_MONTH = 90
	MORE_THAN_YEAR = 400
	DURATION_CHOICES = (
		(LESS_THAN_MONTH, 'less than one month'),
		(MORE_THAN_MONTH, 'more than one month'),
		(MORE_THAN_YEAR, 'more than a year'),
	)
	TERRIBLE = 'TR'
	BAD = 'BD'
	GOOD = 'GD'
	EXCELLENT = 'EC'
	RATING_CHOICES = (
		(TERRIBLE, 'terrible'),
		(BAD, 'bad'),
		(GOOD, 'good'),
		(EXCELLENT, 'excellent'),
	)
	user = models.ForeignKey(CustomUser)
	item = models.ForeignKey(Item)
	duration = models.PositiveSmallIntegerField(choices=DURATION_CHOICES)
	rating = models.CharField(max_length=2, choices=RATING_CHOICES)

post_save.connect(save_item_sphinx, sender=Item)
pre_delete.connect(delete_item_sphinx, sender=Item)