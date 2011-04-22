from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from django.contrib.gis import admin

admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    (r'^$','pkumap.index.index'),
	(r'^index','pkumap.index.index2'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^poi/',include('pkumap.pois.urls')),
    (r'^route/',include('pkumap.route.urls'))
)

if settings.DEBUG:
	urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
		{'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
