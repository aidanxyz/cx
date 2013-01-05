from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from customauth.models import CustomUser

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('email', 'full_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Password don't match")
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser

	def clean_password(self):
		return self.initial["password"]

class CustomUserAdmin(UserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'full_name', 'password')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		('Personal Info', {'fields': ('full_name',)}),
		('Permissions', {'fields': ('is_admin',)}),
		('Important dates', {'fields': ('last_login',)}),
	)
	add_fieldsets = (
		('None', {
			'classes': ('wide',),
			'fields': ('email', 'full_name', 'password1', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)
# ... and, since we're not using Django's builtin Permissions,
# unregister the Group model from admin
admin.site.unregister(Group)