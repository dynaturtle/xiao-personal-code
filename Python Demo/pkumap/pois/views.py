#Create your views here.
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import MultiPoint
from pkumap.pois.models import CBuilding,CEDepartment,CVDepartment,CScene
import json
import time
#import memcache
from django.core.cache import cache

def queryallkey(request):
	"""all type"""
	keyword = request.REQUEST['q'];	
	return HttpResponse(queryallkeybystr(keyword))

def queryallkeybystr(key):
	"""all type"""
	begintime = time.time()
	keyword = key	
	#get from cache
	mcstr = "poisqak"+keyword
	str = cache.get(mcstr)
	if str != None:
		endtime = time.time()
		print endtime-begintime
		return str

	#get from db
	result = []
	vd = fnGetVDepartment(keyword)
	ed = fnGetEDepartment(keyword)
	sc = fnGetScene(keyword)
	bd = fnGetBuilding(keyword)
	
	for i in vd:
		result.append(i)
	for i in ed:
		result.append(i)
	for i in sc:
		result.append(i)
	for i in bd:
		result.append(i)

	str = json.dumps(result)
	cache.set(mcstr,str,60*15)

	endtime = time.time()
	print endtime-begintime
	#~end from db
	return str

def queryallkeyautocomplete(request):
        """all type"""
        keyword = request.REQUEST['q'];

        result = []
        vd = fnGetVDepartment(keyword)
        ed = fnGetEDepartment(keyword)
        sc = fnGetScene(keyword)
        bd = fnGetBuilding(keyword)

        for i in vd:
                result.append(i['name'].strip())
        for i in ed:
                result.append(i['name'].strip())
        for i in sc:
                result.append(i['name'].strip())
        for i in bd:
                result.append(i['name'].strip())

        str = json.dumps(result)

        return HttpResponse(str)


def querydepartment(request):
	"""return both vitual department and entity department"""
	keyword = request.REQUEST['q']

	vresult = fnGetVDepartment(keyword)
	eresult = fnGetEDepartment(keyword)

	result = []
	for i in vresult:
		result.append(i)
	for i in eresult:
		result.append(i)

	str = json.dumps(result)

	return HttpResponse(str)

def querybuilding(request):
	"""return the building query"""
	keyword = request.REQUEST['q']
	result = fnGetBuilding(keyword)

	str = json.dumps(result)

	return HttpResponse(str)


def queryscene(request):
	"""return the scenary query"""
	keyword = request.REQUEST['q']
	result = fnGetScene(keyword)
	
	str = json.dumps(result)
	
	return HttpResponse(str)

def getbuildingbyid(request,b_id):
	"""get the building info by id"""
	result = []
	try:
		b = CBuilding.objects.get(pk=b_id)
		building_entry = {}
		building_entry['type'] = "building"
		building_entry['id'] = b_id
		building_entry['name'] = b.bname
		building_entry['footprint'] = b.loc.wkt
		attributes_entry = {}
		attributes_entry['picurl'] = b.bphoto
		building_entry['attributes'] = attributes_entry
		result.append(building_entry)
	except CBuilding.DoesNotExist:
		result = []
	
	str = json.dumps(result)
	return HttpResponse(str)

"""query the scenary and return list"""
def fnGetScene(keyword):
	result = []
	
	if keyword == "":
		return result
	
	scene_list = CScene.objects.filter(sname__contains=keyword).order_by('count').reverse()
	for i in scene_list:
		i.count = i.count+1
		i.save()

		scene_entry = {}
		scene_entry['type'] = "scene"
		scene_entry['name'] = i.sname
		scene_entry['id'] = i.pk
		scene_entry['footprint'] = i.loc.wkt
		attribute_entry = {}
		attribute_entry['picurl'] = i.sphoto
		attribute_entry['desc'] = i.sdesc
		scene_entry['attributes']=attribute_entry

		result.append(scene_entry)
	
	return result

"""query all the building"""
def fnGetBuilding(keyword):
	result = []

	if keyword == "":
		return result
	
	build_list = CBuilding.objects.filter(bname__contains=keyword).order_by('count').reverse()
	for i in build_list:
		i.count = i.count+1
		i.save()

		build_entry={}

		build_entry['type'] = "building"
		build_entry['name'] = i.bname
		build_entry['id'] = i.pk
		build_entry['footprint'] = i.loc.wkt
		attribute_entry = {}
		attribute_entry['picurl'] = i.bphoto
		build_entry['attributes'] = attribute_entry
		
		result.append(build_entry)

	return result

"""query all the virtual department"""
def fnGetVDepartment(keyword):
	result = []

	if keyword == "":
		return result

	v_depart_list = CVDepartment.objects.filter(vname__contains=keyword).order_by('count').reverse()
	for i in v_depart_list:
		i.count = i.count+1
		i.save()

		vd_entry = {}
		vd_entry['type'] = 'department'
		vd_entry['name'] = i.vname
		vd_entry['id'] = i.pk

		p = Point(0,0)
		mp = MultiPoint(p)
		mp.remove(p)
		attributes_entry = {}
		attributes_entry['url'] = i.vlink
		children_list = []

		#e_depart_list = CEDepartment.objects.filter(cvdepartment_cedepartment_exact=i)
		e_depart_list = CEDepartment.objects.filter(evid__pk__exact=i.pk)
		for j in e_depart_list:
			j.count = j.count+1
			j.save()

			mp.append(j.ebid.loc)
			
			children_item = {}
			children_item['id'] = j.pk
			children_item['name'] = j.ename
			children_list.append(children_item)

		attributes_entry['children'] = children_list
		
		vd_entry['footprint'] = mp.wkt
		vd_entry['attributes'] = attributes_entry
		
		result.append(vd_entry)
	
	return result

"""query all the entity department"""
def fnGetEDepartment(keyword):
	result = []

	if keyword == "":
		return result

	e_depart_list = CEDepartment.objects.filter(ename__contains=keyword).order_by('count').reverse()
	for i in e_depart_list:
		i.count = i.count+1
		i.save()

		ed_entry={}
		ed_entry['type']='department'
		ed_entry['name'] = i.ename
		ed_entry['id'] = i.pk
		#if the ebid is not assign a value, how to detect this?
		#does not exist raised
		ed_entry['footprint'] = i.ebid.loc.wkt
		attributes_entry = {}
		building_entry = {}
		building_entry['name'] = i.ebid.bname
		building_entry['id'] = i.ebid.pk
		attributes_entry['building'] = building_entry
		attributes_entry['picurl'] = i.ephoto
		attributes_entry['url'] = i.elink
		ed_entry['attributes'] = attributes_entry

		result.append(ed_entry)

	return result
