from django.http import HttpResponse
from django.contrib.gis.geos import Point
from models import *
from pkumap.pois.models import *
import json

def getExactRoutePoi(request):
	"""
	get a route poi by the name
	if name is duplicate,then record the error
	"""
	rpname = request.REQUEST['q']
	#print rpname

	rplist = RoutePoiDB.objects.filter(name__exact=rpname)
	resultitem = {}
	result = []
	if rplist.count() > 1:
		routeerrorfile = file('routeerrorfile','a')
		#errorstr = unicode(rpname,"utf-8")+" name duplicate"
		errorstr = "name duplicate"
		routeerrorfile.write(errorstr)
		routeerrorfile.close()
		resultitem = _routePoi2entry(rplist[0])
		result.append(resultitem)
	elif rplist.count() == 1:
		resultitem = _routePoi2entry(rplist[0])
		#comment is not good
		#rplist[0].searchcount = rplist[0].searchcount + 1
		#rplist[0].save()
		tmp = rplist[0]
		tmp.searchcount = tmp.searchcount + 1
		tmp.save()
		result.append(resultitem)
	else:
		result = []
	
	return HttpResponse(json.dumps(result))
		
def _routePoi2entry(rp):
	"""transfer a routepoi to an entry"""
	pentry = {}
	
	pentry['type'] = "routepoi"
	pentry['id'] = rp.pk
	pentry['name'] = rp.name
	pentry['footprint'] = rp.geom.wkt
	
	attributes_entry = {}
	attributes_entry['alias'] = rp.alias
	attributes_entry['searchcount'] = rp.searchcount
	pentry['attributes'] = attributes_entry

	return pentry

def getPossibleRoutePoi(request):
	"""
	get the possible route poi
	"""
	rn = request.REQUEST['q']
	allrp = RoutePoiDB.objects.order_by('searchcount').reverse()

	resultlist = []
	for p in allrp:
		name = p.name
		if _orderSatisfy(rn,name) == 1:
			#resultlist.append(_routePoi2entry(p))
			resultlist.append(name)

	result = []
	len = 10
	if resultlist.__len__() < 10:
		len = resultlist.__len__()
	for i in range(0,len):
		result.append(resultlist[i])
	

	return HttpResponse(json.dumps(result))

def _orderSatisfy(subname,name):
	"""
	if subname is sub of name
		return 1
	else 
		return 0
	testcast1:
	s1:liijao(zhongwen)
	s2:likejiaoxuelou(zhongwen)
	testcase2:
	s1:ab
	s2:acb
	"""
	i = 0
	curindex = 0
	for i in range(0,len(subname)):
		#print i
		tmp =  name.find(subname[i],curindex)
		#print tmp
		#print ""
		if tmp == -1:
			return 0
		else:
			curindex = tmp+1
	
	return 1

def _transferPoi2RoutePoi():
	"""
	note that all search count set to 0
	"""
	buildings = CBuilding.objects.all()
	for i in buildings:
		t = RoutePoiDB()
		if len(i.bname) > 20:
			t.name = i.bname[0:20].strip()
		else:
			t.name = i.bname.strip()
		if len(i.balias) > 100:
			t.alias = i.balias[0:100].strip()
		else:
			t.alias = i.balias.strip()
		t.geom = i.loc
		t.searchcount = 0
		t.save()
	
	scenes = CScene.objects.all()
	for i in scenes:
		t = RoutePoiDB()
		if len(i.sname) > 20:
			t.name = i.sname[0:20].strip()
		else:
			t.name = i.sname.strip()
		if len(i.salias) > 100:
			t.alias = i.salias[0:100].strip()
		else:
			t.alias = i.salias.strip()
		t.geom = i.loc
		t.searchcount = 0
		t.save()
