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
	
	def __unicode__(self):
		return self.name

class ItemAddForm(ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'category')

post_save.connect(save_item_sphinx, sender=Item)
pre_delete.connect(delete_item_sphinx, sender=Item)