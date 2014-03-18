from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from views import *

handler404 = 'views.error_404'

urlpatterns = patterns('',
    (r'^$', index),
    (r'^index/$', index),
    (r'^special/$', special),
    (r'^qna/$', qna_index),
    (r'^qna/all/$', qna_list),
    (r'^senior/$', senior),
    (r'^about/$', about),
    (r'^q/$', q_form),
    (r'^q/success/(-?\d+)/$', q_success),
    (r'^tag/$', tag_list),
    (r'^tag/(.+)/$', tag_view),
    (r'^university/$', university_list),
    (r'^university/(.+)/$', university_view),
    (r'^view/(-?\d+)/$', qna_view),
    (r'^view/auth/(-?\d+)/$', qna_auth),
    (r'^search/(.+)/$', search),
    (r'^comment/(\d+)/$', comment_view),
    (r'^answer/(\d+)/thank/$', answer_thank),
    (r'^dump/$', dump),

    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_PATH}),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'})
)
