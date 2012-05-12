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
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/32.ico'}),
    (r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),

    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^item/$', 'item.views.inbox', name='inbox'),
    url(r'^item/all/$', 'item.views.get_items', name='get_items'),
    url(r'^attribute/all/$', 'item.views.get_attributes', name='get_attributes'),
    url(r'^item/add/$', 'item.views.add_item', name='add_item'),
    url(r'^item/(?P<item_pk>\d+)/$', 'item.views.get_item', name='get_item'),
    url(r'^attribute/add/$', 'item.views.add_attribute', name='add_attribute'),
    url(r'^command/$', 'item.views.run_command', name='run_command'),
    url(r'', include('social_auth.urls')),
)
