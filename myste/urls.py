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
    url(r'accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'../opt/templates/login.html'}),
    url(r'day/$', 'opt.views.dayReport'),
    url(r'^login/$', 'opt.views.login'),
    url(r'^upload/$', 'opt.views.upload'),
    url(r'^register/$', 'opt.views.register'),
    url(r'^index/$', 'opt.views.index'),
    url(r'^dayAccount/$', 'opt.views.dayAccountReport'),
    url(r'^week/$', 'opt.views.weekReport'),
    url(r'^weekAccount/$', 'opt.views.weekAccountReport'),
    url(r'^coverage/$', 'opt.views.coverage'),
)
urlpatterns +=staticfiles_urlpatterns()
