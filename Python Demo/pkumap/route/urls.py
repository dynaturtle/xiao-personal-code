from django.conf.urls.defaults import *
#from django.views.decorators.cache import cache_page
import views

urlpatterns = patterns('',
    #(r'^placename/$','pkumap.route.views.namequery'),
    (r'^coordinate/$','pkumap.route.views.getRoute'),
    #(r'^coordinate/$',cache_page(views.getRoute,60*15)),
    (r'^exactroutepoi/$','pkumap.route.routepoi.getExactRoutePoi'),
    (r'^possibleroutepoi/$','pkumap.route.routepoi.getPossibleRoutePoi'),
    )
