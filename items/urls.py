from django.conf.urls import patterns, include, url

urlpatterns = patterns('items.views',
	url(r'^$', 'index'),
	url(r'^(?P<item_id>\d+)/$', 'view'), # items/25
	url(r'^add/', 'add'),
	url(r'^search/', 'search'),
)

urlpatterns += patterns('reviews.views', 
	url(r'^(?P<item_id>\d+)/feedbacks/add/$', 'add_feedback'), # items/25/feedbacks/add
)