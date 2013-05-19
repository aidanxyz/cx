from django.db import models
from django.conf import settings
from django import forms
from django.db.models.signals import post_save, pre_delete
from items.receivers import save_item_sphinx, delete_item_sphinx
from items.item_utils import get_item_image_path
import Image
from django.utils import timezone
from contextlib import closing
import MySQLdb
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

class SpecificationType(models.Model):
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=256)
	categories = models.ManyToManyField(Category)

	def __unicode__(self):
		return self.name

class Specification(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=256)
	spectype = models.ForeignKey(SpecificationType)

	class Meta:
		unique_together = ('name', 'spectype')

	def __unicode__(self):
		return self.name

class ItemPossibleDuplicates(models.Model):
	str_list = models.CharField(max_length=512)
	number = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return self.str_list

class Item(models.Model):
	name = models.CharField(max_length=200, unique=True)
	date_created = models.DateTimeField('date created')
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	category = models.ForeignKey(Category)
	cover_image = models.ForeignKey('ItemImage', related_name="cover_image", null=True, blank=True)
	is_active = models.BooleanField(default=True, blank=True)
	is_approved = models.BooleanField(default=False, blank=True)
	latest_feedback = models.ForeignKey('reviews.Feedback', related_name="items_latest_set", null=True, blank=True)
	views_count = models.PositiveIntegerField(default=0)
	pros_count = models.PositiveIntegerField(default=0)
	cons_count = models.PositiveIntegerField(default=0)
	possible_duplicates = models.OneToOneField(ItemPossibleDuplicates, null=True, blank=True)
	specifications = models.ManyToManyField(Specification)
	avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	reviewers_count = models.PositiveIntegerField(default=0)

	class Meta:
		permissions = (
			("moderate_items", "Can access views related to item moderation"), 
		)

	def get_similar_item_ids(self, name=None):
		if not name:
			name = self.name

		connection = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
		with closing(connection.cursor()) as cursor:
			cursor.execute("select * from items_item where match('@name %s')" % str(name)) # is it safe?
			ids = [row[0] for row in cursor.fetchall()] # is it efficient?	
		connection.close()
		return ids

	def __unicode__(self):
		return 'name:' + self.name + ',' + 'category:' + self.category.name


post_save.connect(save_item_sphinx, sender=Item)
pre_delete.connect(delete_item_sphinx, sender=Item)

class ItemAddForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('name', 'category')

class ItemApprovalHistory(models.Model):
	item = models.ForeignKey(Item)
	moderator = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_approved = models.DateTimeField()

class ItemDeactivationReason(models.Model):
	reason = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.reason

class ItemDeactivationHistory(models.Model):
	item = models.ForeignKey(Item)
	moderator = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_deactivated = models.DateTimeField()
	reason = models.ForeignKey(ItemDeactivationReason)
	duplicate_of = models.ForeignKey(Item, related_name='duplicate_of', null=True, blank=True)

class ItemDeactivationForm(forms.ModelForm):
	class Meta:
		model = ItemDeactivationHistory
		fields = ('reason', 'duplicate_of')

class ItemEditReason(models.Model):
	reason = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.reason

class ItemEditHistory(models.Model):
	item = models.ForeignKey(Item)
	moderator = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_edited = models.DateTimeField()
	reason = models.ForeignKey(ItemEditReason)
	other_reason = models.CharField(max_length=200, null=True)
	old_value = models.CharField(max_length=200)

class ItemEditForm(forms.Form):
	# Item
	name = forms.CharField(max_length=200)
	category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select, empty_label=None)
	# Reason
	reason = forms.ModelChoiceField(queryset=ItemEditReason.objects.all(), widget=forms.RadioSelect, empty_label=None)
	other_reason = forms.CharField(max_length=200, required=False)

	"""
	https://docs.djangoproject.com/en/dev/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
	"""
	def clean(self):
		cleaned_data = super(ItemEditForm, self).clean()
		reason = cleaned_data.get('reason')
		other_reason = cleaned_data.get('other_reason', None)
		
		if reason and reason.reason == 'Other' and not other_reason:
			msg = u"Other reason must be specified"
			self._errors["other_reason"] = self.error_class([msg])
			del cleaned_data['other_reason']

		return cleaned_data

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
		ordering = ('value',)

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
		fields = ('duration', 'rating',)

class ItemImage(models.Model):
	item = models.ForeignKey(Item)
	image = models.ImageField(upload_to=get_item_image_path)
	image_mini_thumb = models.ImageField(upload_to="gallery_thumb_buggy_imgs", blank=True)
	image_cover_thumb = models.ImageField(upload_to="gallery_thumb_buggy_imgs", blank=True, null=True)
	image_gallery_thumb = models.ImageField(upload_to="gallery_thumb_buggy_imgs", 
		blank=True)
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	date_uploaded = models.DateTimeField()

	class Meta:
		unique_together = ('image', 'image')

	def save(self, request=None, *args, **kwargs):
		super(ItemImage, self).save(*args, **kwargs)
		image_full_path = settings.MEDIA_ROOT + self.image.name
		orignal_image = Image.open(image_full_path)
		width, height = orignal_image.size
		
		# let's -D-RY some images :)
		
		# creating mini_thumb
		new_width = 70
		path = 'itemimage_mini_thumbs/' + self.image.name.split('/')[1]
		if width > new_width:
			new_height = int(height * new_width / width)
			mini_thumb = orignal_image.resize((new_width, new_height), Image.ANTIALIAS)
			mini_thumb.save(settings.MEDIA_ROOT + path, "JPEG")
		else:
			path = image_full_path
		self.image_mini_thumb = path
		
		# creating gallery_thumb
		new_width = 200
		path = 'itemimage_gallery_thumbs/' + self.image.name.split('/')[1]
		if width > new_width:
			new_height = int(height * new_width / width)
			gallery_thumb = orignal_image.resize((new_width, new_height), Image.ANTIALIAS)
			gallery_thumb.save(settings.MEDIA_ROOT + path, "JPEG")			
		else:
			path = image_full_path
		self.image_gallery_thumb = path
		
		# creating cover_thumb
		new_width = 940
		if width > new_width:
			new_height = int(height * new_width / width)
			cover_thumb = orignal_image.resize((new_width, new_height), Image.ANTIALIAS)
			path = 'itemimage_cover_thumbs/' + self.image.name.split('/')[1]
			cover_thumb.save(settings.MEDIA_ROOT + path, "JPEG")
			self.image_cover_thumb = path
		
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

class Price(models.Model):
	item = models.ForeignKey(Item)
	value = models.DecimalField(max_digits=10, decimal_places=2)
	source_url = models.URLField()
	date_added = models.DateTimeField()
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	is_active = models.BooleanField(default=True)
	is_approved = models.BooleanField(default=False)
	resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="resolver", null=True)

class PriceAddForm(forms.ModelForm):
	class Meta:
		model = Price
		fields = ('value', 'source_url',)
