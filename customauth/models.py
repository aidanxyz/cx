from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from items.models import Item

class CustomUserManager(BaseUserManager):
	def create_user(self, email, full_name, password=None):
		"""
		Creates and saves a User with the given email, full_name and password
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=CustomUserManager.normalize_email(email),
			full_name=full_name,
		)

		user.set_password(password)
		user.save(using=self._db) # -> ?
		return user

	def create_superuser(self, email, full_name, password):
		"""
		Creates and saves a superuser with the given email, full_name
		and password.
		"""
		user = self.create_user(email, full_name, password)
		user.is_admin = True
		user.save(using=self._db)
		return user

class CustomUser(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email_address',
		max_length=255,
		unique=True,
		db_index=True,
	)
	full_name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	items_used = models.ManyToManyField(Item)

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
		return self.is_admin