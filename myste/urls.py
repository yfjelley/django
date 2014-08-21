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
    url(r'^select/$', 'opt.views.selection'),
    url(r'^week/$', 'opt.views.opt_week'),
    url(r'^site/$', 'opt.views.opt_site'),
    url(r'^boot/$', 'opt.views.boot'),
    url(r'^index/$', 'opt.views.index'),
    url(r'^dayReport/$', 'opt.views.dayReport'),
    url(r'^table/$', 'opt.views.table'),

    url(r'^weekReport/$', 'opt.views.weekReport'),
    url(r'^monthReport/$', 'opt.views.monthReport'),
#    url(r'^index/$', 'opt.views.index'),
#    url(r'^ajax_deal/$','opt.views.ajax_deal'),
    url(r'^test1/$', 'opt.views.opt_data'),
)
urlpatterns +=staticfiles_urlpatterns()
