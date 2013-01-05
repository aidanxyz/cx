from django.conf.urls import patterns, include, url

urlpatterns = patterns('items.views',
	url(r'^$', 'index'),
	url(r'^add/', 'add'),
)