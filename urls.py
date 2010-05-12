from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^PhoneSearch/', include('PhoneSearch.foo.urls')),
    (r'^$', 'PhoneSearch.main.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':'/Users/dave/projects/PhoneSearch/static' }),
    (r'^search$', 'PhoneSearch.main.views.search'),
    (r'^search/(?P<page>[0-9]+)/$', 'PhoneSearch.main.views.search'),
    (r'^similar$', 'PhoneSearch.main.views.similar'),
    (r'^similar/(?P<page>[0-9]+)/$', 'PhoneSearch.main.views.similar')
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
