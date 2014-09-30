from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myste.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'opt.views.login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^day/$', 'opt.views.dayReport'),
    url(r'^login/$', 'opt.views.login'),
    url(r'^regist/$', 'opt.views.regist'),
    url(r'^index/$', 'opt.views.index'),
    url(r'^dayAccount/$', 'opt.views.dayAccountReport'),
    url(r'^week/$', 'opt.views.weekReport'),
    url(r'^weekAccount/$', 'opt.views.weekAccountReport'),
)
urlpatterns +=staticfiles_urlpatterns()
