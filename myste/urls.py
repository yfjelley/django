from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myste.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^opt/$', 'opt.views.opt'),
    url(r'^boot/$', 'opt.views.boot'),
    url(r'^day/$', 'opt.views.dayReport'),
    url(r'^week/$', 'opt.views.weekReport'),
    url(r'^weekAccount/$', 'opt.views.weekReportAccount'),
    url(r'^month/$', 'opt.views.monthReport'),
    url(r'^table/$', 'opt.views.table'),
)
urlpatterns +=staticfiles_urlpatterns()
