from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url(r'^$', 'thweb.views.home', name='home'),
    url(r'^user/$', 'thweb.views.user', name='user'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
)
