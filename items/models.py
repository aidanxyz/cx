from django.db import models
from django.conf import settings
from django import forms
from django.db.models.signals import post_save, pre_delete
from items.receivers import save_item_sphinx, delete_item_sphinx
from items.item_utils import get_item_image_path
import Image

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
	cover_image = models.ForeignKey('ItemImage', related_name="cover_image", null=True)
	STATUS_CHOICES = (
		('NC', 'Not checked'),
		('C', 'Checked'),
		('NA', 'Not active')
	)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NC')
	latest_feedback = models.ForeignKey('reviews.Feedback', related_name="items_latest_set", null=True)
	views_count = models.PositiveIntegerField(default=0)
	pros_count = models.PositiveIntegerField(default=0)
	cons_count = models.PositiveIntegerField(default=0)
	
	def __unicode__(self):
		return self.name

class ItemAddForm(forms.ModelForm):
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

class ItemUsageForm(forms.ModelForm):
	class Meta:
		model = ItemUsageExperience
		fields = ('duration', 'rating')

class ItemImage(models.Model):
	item = models.ForeignKey(Item)
	image = models.ImageField(upload_to=get_item_image_path)
	# image_mini_thumb = models.ImageField(blank=True, null=True)
	image_gallery_thumb = models.ImageField(upload_to="gallery_thumb_buggy_imgs", 
		blank=True, null=True)

	class Meta:
		unique_together = ('image', 'image')

	def save(self, request=None, *args, **kwargs):
		super(ItemImage, self).save(*args, **kwargs)
		image_full_path = settings.MEDIA_ROOT + self.image.name
		# creating gallery thumbnail
		gallery_thumb = Image.open(image_full_path)
		if gallery_thumb.size[1] > 200:
			new_width = int(200 * gallery_thumb.size[0] / gallery_thumb.size[1])
			gallery_thumb = gallery_thumb.resize((new_width, 200), Image.ANTIALIAS)
			path = 'itemimage_gallery_thumbs/' + self.image.name.split('/')[1]
			gallery_thumb.save(settings.MEDIA_ROOT + path, "JPEG")
			# saving the model
			self.image_gallery_thumb = path
			super(ItemImage, self).save(*args, **kwargs)

class ItemImageUploadForm(forms.Form):
	image = forms.ImageField()

	def clean_image_size(self):
		image = self.cleaned_data.get('image', False)
		if image:
			if image._size > 2097152:
				raise ValidationError("Image is too large")
			return image
		else:
			raise ValidationError("Couldn't read image file")