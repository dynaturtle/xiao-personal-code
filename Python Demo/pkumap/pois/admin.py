from pkumap.pois.models import CBuilding,CScene,CVDepartment,CEDepartment
#from django.contrib import admin
from django.contrib.gis import admin

#admin.site.register(POI,admin.GeoModelAdmin)
admin.GeoModelAdmin.openlayers_url = "/site_media/lib/openlayers/OpenLayers.js"
admin.site.register(CBuilding,admin.GeoModelAdmin)
admin.site.register(CScene,admin.GeoModelAdmin)
admin.site.register(CVDepartment,admin.GeoModelAdmin)
admin.site.register(CEDepartment,admin.GeoModelAdmin)
