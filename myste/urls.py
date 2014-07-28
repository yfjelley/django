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
#    url(r'^index/$', 'opt.views.index'),
#    url(r'^ajax_deal/$','opt.views.ajax_deal'),
    url(r'^test1/$', 'opt.views.opt_data'),
)
urlpatterns +=staticfiles_urlpatterns()
