from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'customauth/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/items'}),
	url(r'^register/$', 'customauth.views.register_user'),
)