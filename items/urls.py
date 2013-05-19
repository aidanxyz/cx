from django.conf.urls import patterns, include, url

urlpatterns = patterns('items.views',
	url(r'^$', 'explore'),
	url(r'^explore/$', 'explore'),
	url(r'^(?P<item_id>\d+)/$', 'view'), # items/25
	url(r'^(?P<item_id>\d+)/usage/add/$', 'add_usage_experience'), # items/25/used
	url(r'^add/', 'add'),
	url(r'^search/', 'search'),
	url(r'^moderate/', 'moderate_items'),
	url(r'^(?P<item_id>\d+)/approve/$', 'approve_item'),
	url(r'^(?P<item_id>\d+)/deactivate/$', 'deactivate_item'),
	url(r'^(?P<item_id>\d+)/edit/$', 'edit_item'),
	url(r'^(?P<item_id>\d+)/duplicates/$', 'get_possible_duplicates'),
	url(r'^(?P<item_id>\d+)/gallery/$', 'view_item_images'),
	url(r'^(?P<item_id>\d+)/gallery/add/$', 'add_item_image'),
	url(r'^prices/moderate/', 'moderate_prices'),
	url(r'^(?P<item_id>\d+)/prices/add/', 'add_price'),
	url(r'^prices/(?P<price_id>\d+)/approve/', 'approve_price'),
	url(r'^prices/(?P<price_id>\d+)/ignore/', 'ignore_price'),
	url(r'^(?P<item_id>\d+)/set_cover_image/', 'set_cover_image'),
	url(r'^latest/(?P<number>\d+)/$', 'get_latest'),
	url(r'^(?P<item_id>\d+)/stats/$', 'stats_page'),
	url(r'^(?P<item_id>\d+)/get_stats/$', 'get_stats'),
)

urlpatterns += patterns('reviews.views', 
	url(r'^(?P<item_id>\d+)/feedbacks/add/$', 'add_feedback'), # items/25/feedbacks/add
)