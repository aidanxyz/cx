from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.forms import ModelForm
from django.utils import timezone

class CustomUserManager(BaseUserManager):
	def create_user(self, email, full_name, year_of_birth, gender, password=None):
		"""
		Creates and saves a User with the given email, full_name and password
		"""
		if not email:
			raise ValueError('Users must have an email address')

		if year_of_birth > (timezone.now().year - 10) or year_of_birth < (timezone.now().year - 100):
			raise ValueError('Year of birth is out of bounds')

		user = self.model(
			email=CustomUserManager.normalize_email(email),
			full_name=full_name,
			year_of_birth=year_of_birth,
			gender=gender
		)

		user.set_password(password)
		user.save(using=self._db) # -> ?
		return user

	def create_superuser(self, email, full_name, year_of_birth, gender, password):
		"""
		Creates and saves a superuser with the given email, full_name
		and password.
		"""
		user = self.create_user(email, full_name, year_of_birth, gender, password)
		user.is_superuser = True
		user.save(using=self._db)
		return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	full_name = models.CharField(max_length=255)
	year_of_birth = models.PositiveSmallIntegerField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	email = models.EmailField(
		verbose_name='email_address',
		max_length=255,
		unique=True,
		db_index=True,
	)
	is_active = models.BooleanField(default=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name', 'year_of_birth', 'gender']

	items_used = models.ManyToManyField('items.Item', through="items.ItemUsageExperience")

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		return self.email

	def __unicode__(self):
		return self.full_name + ' ' + self.email

	def has_perm(self, perm, obj=None):
		return True;

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_superuser