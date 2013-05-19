from django.conf.urls import patterns, include, url

urlpatterns = patterns('reviews.views',
	url(r'^(?P<feedback_id>\d+)/vote/$', 'vote'), # /2334/vote
    url(r'^(?P<feedback_id>\d+)/unvote/$', 'unvote'), # /2334/unvote
    url(r'^(?P<feedback_id>\d+)/details/$', 'list_details'), # /4556/details/
    url(r'^(?P<feedback_id>\d+)/details/add/$', 'add_detail'), # /4556/details/add
    url(r'^(?P<feedback_id>\d+)/priority/set/$', 'set_priority'), # /4556/priority/set
    url(r'^(?P<feedback_id>\d+)/priority/unset/$', 'unset_priority'), # /4556/priority/unset
    url(r'^(?P<feedback_id>\d+)/suggest_edit/$', 'suggest_edit'), # /2334/vote
    url(r'^(?P<feedback_id>\d+)/edit/$', 'edit_feedback'), 
    url(r'^moderate/$', 'moderate_feedback'), 
    url(r'^suggestions/(?P<suggestion_id>\d+)/accept/$', 'accept_feedbackeditsuggestion'), 
    url(r'^suggestions/(?P<suggestion_id>\d+)/ignore/$', 'ignore_feedbackeditsuggestion'), 
    url(r'^search/$', 'search_feedback')
)

urlpatterns += patterns('reviews.views', 
	url(r'^(?P<item_id>\d+)/feedbacks/add/$', 'add_feedback'), # items/25/feedbacks/add
)