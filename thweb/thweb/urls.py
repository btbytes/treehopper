from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
                       url(r'^$', 'thweb.views.home', name='home'),
                       url(r'^user/$', 'thweb.views.user', name='user'),
                       url(r'^repo/(?P<repo_name>\w+)$', 'thweb.views.repoview', name='repoview'),
                       url(r'^repo/(?P<repo_name>\w+)/calview$', 'thweb.views.calview', name='calview'),
                       url(r'^repo/(?P<repo_name>\w+)/caldata/(?P<year>\d{4})$', 'thweb.views.caldata', name='caldata'),
                       url(r'^repo/(?P<repo_name>\w+)/commitvol$', 'thweb.views.commitvol', name='commitvol'),


    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
)
