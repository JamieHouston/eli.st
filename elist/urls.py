#from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     url(r'^$', 'account.views.home', name='home'),
#     url(r'^account/', include('account.urls')),

#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     #url(r'^admin/', include(admin.site.urls)),
#     url(r'', include('social_auth.urls')),
# )


from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from account.views import home, done, logout, error, form


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)
