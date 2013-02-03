from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.views',
	url(r'^feedback/add/$', 'add_feedback'),
	url(r'^vote/$', 'vote'),
	url(r'^unvote/$', 'unvote'),
)