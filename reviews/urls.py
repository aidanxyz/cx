from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews',
	url(r'^feedback/add/$', 'feedback_views.add'),
)