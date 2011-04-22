from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^auto/$','pkumap.pois.views.queryallkeyautocomplete'),
	(r'^$','pkumap.pois.views.queryallkey'),
#	(r'^name/$','pkumap.pois.views.querynamekey'),
	(r'^building/$','pkumap.pois.views.querybuilding'),
	(r'^department/$','pkumap.pois.views.querydepartment'),
	(r'^scene/$','pkumap.pois.views.queryscene'),
	(r'^building/(?P<b_id>\d+)/$','pkumap.pois.views.getbuildingbyid'),
	)
