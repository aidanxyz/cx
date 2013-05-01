from django.conf.urls import patterns, include, url

urlpatterns = patterns('items.views',
	url(r'^$', 'index'),
	url(r'^(?P<item_id>\d+)/$', 'view'), # items/25
	url(r'^(?P<item_id>\d+)/usage/add/$', 'add_usage_experience'), # items/25/used
	url(r'^add/', 'add'),
	url(r'^search/', 'search'),
	url(r'^(?P<item_id>\d+)/gallery/$', 'view_item_images'),
	url(r'^(?P<item_id>\d+)/gallery/add/$', 'add_item_image'),
)

urlpatterns += patterns('reviews.views', 
	url(r'^(?P<item_id>\d+)/feedbacks/add/$', 'add_feedback'), # items/25/feedbacks/add
)