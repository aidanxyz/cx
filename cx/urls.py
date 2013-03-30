from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cx.views.home', name='home'),
    # url(r'^cx/', include('cx.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Custom URLs
    url(r'^items/', include('items.urls')),
    url(r'^customauth/', include('customauth.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feedbacks/(?P<feedback_id>\d+)/vote/$', 'reviews.views.vote'), # /feedbacks/2334/vote
    url(r'^feedbacks/(?P<feedback_id>\d+)/unvote/$', 'reviews.views.unvote'), # /feedbacks/2334/unvote
    url(r'^feedbacks/(?P<feedback_id>\d+)/details/$', 'reviews.views.list_details'), # /feedbacks/4556/details/
    url(r'^feedbacks/(?P<feedback_id>\d+)/details/add/$', 'reviews.views.add_detail'), # /feedbacks/4556/details/add
    url(r'^feedbacks/search/$', 'reviews.views.search_feedback')
)
