# Create your views here.
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.gdal import *
import math
import re
from models import *
import json
import time
#from django.views.decorators.cache import cache_page
from django.core.cache import cache

"""
input:Control Point 1,Control Point 2
output:LineString
if no route, return (0,0)->(0,0)
"""
def getRouteCC(cp1,cp2):
	"""basic get from the db"""
	"""is django possible for the db not define in the models?"""
	"""simple django psql code"""
	
	#Point p1 = Point(cp1)
	#Point p2 = Point(cp2)
	#c1 = ControlPointDB.objects.filter(geom__exact=p1)
	#c2 = COntrolPointDB.objects.filter(geom__exact=p2)
	#RouteDB.objects.filter(startPt__exact=c1&endPt__exact=c2)

	route_list = RouteDB.objects.all()
	for route in route_list:
		p1 = route.geom.tuple[0]
		p2 = route.geom.tuple[route.geom.num_points-1]
		if p1[0] == cp1[0] and p1[1] == cp1[1] and p2[0] == cp2[0] and p2[1] == cp2[1]:
#		thres = 3
#		if math.fabs(p1[0]-cp1[0])<thres and math.fabs(p1[1]-cp1[1])<thres and math.fabs(p2[0]-cp2[0])<thres and math.fabs(p2[1]-cp2[1])<thres:
			return route.geom
	return LineString((0,0),(0,0))

"""
query routedb by start_pt and end_pt
"""
def getRouteCC2(cp1,cp2):
	p1 = Point(cp1)
	p2 = Point(cp2)
	c1 = ControlPointDB.objects.filter(geom__exact=p1)
	c2 = ControlPointDB.objects.filter(geom__exact=p2)
	r = RouteDB.objects.filter(startPt__exact=c1[0]).filter(endPt__exact=c2[0])
	if r.count() != 0:
		return r[0].geom
	return LineString((0,0),(0,0))

"""
no use?
input:Control Point 1 , Point of interest 1
output:LineString
"""
def getRouteCP(cp1,poi2):
	cp2r = getMinCP(poi2)
	cp2 = cp2r[0]

	ls = getRouteCC(cp1,cp2)
	#merge the route
	return ls
	
"""
input: Point of Interest 1,2
output: LineString
if no route found,return LineString((0,0),(0,0))
still many condition to think
"""
def getRoutePP(poi1,poi2):
	ppdebug = 0
	#get the control point,path to seg,seg
	cp1r = getMinCP(poi1)
	cp2r = getMinCP(poi2)
	cp1 = cp1r[0]#control point
	cp2 = cp2r[0]

	ls = getRouteCC2(cp1,cp2)
	
	if ls.tuple[0][0] == 0 and ls.tuple[1][0] == 0:
		return LineString((0,0),(0,0))

	resultls = cp1r[1].clone()#path to seg
	beginindex = 0
	endindex = ls.num_points - 1

	#merge the line string
	#process the first seg
	if cp1r[2].tuple[cp1r[2].num_points-1][0] == cp1[0] and cp1r[2].tuple[cp1r[2].num_points-1][1] == cp1[1]:
		cp1r[2].reverse()
	if _beginwithSeg(cp1r[2],ls):
		beginindex = cp1r[2].num_points -1

	if cp2r[2].tuple[0][0] == cp2[0] and cp2r[2].tuple[0][1] == cp2[1]:
		cp2r[2].reverse()
	if _endwithSeg(cp2r[2],ls):
		endindex = endindex - cp2r[2].num_points +1
	
	i = beginindex
	while i <= endindex:
		resultls.append(ls.tuple[i])
		i = i + 1

	cp2r[1].reverse()
	resultls = resultls + cp2r[1]

	return resultls

"""
_beginwithSeg
input:subseg,allseg
output:1,true;0,false
wangxing:2010-5-25:create
testcase:
ls1:((0,0),(1,1))
ls2:((0,0),(1,1),(2,2))
ls3:((0,0),(2,2),(1,1))
ls4:((2,2),(0,0),(1,1))
ls1,ls2
ls1,ls3
"""
def _beginwithSeg(subseg,allseg):
	if allseg.num_points < subseg.num_points:
		return 0
	i = 0
	while i<subseg.num_points:
		if subseg.tuple[i] != allseg.tuple[i]:
			return 0
		i = i+1

	return 1
"""
subseg is part of allseg
return leftpath
"""
def _getBegin(subseg,allseg):
	allseg.tupl

"""
_endwithSeg
input:subseg,allseg
output:1,true;0,false
wangxing:2010-5-15:create
testcase:as above startwithSeg
ls1,ls2
ls1,ls4
"""
def _endwithSeg(subseg,allseg):
	if allseg.num_points < subseg.num_points:
		return 0
	i = 0
	while i < subseg.num_points:
		if allseg.tuple[allseg.num_points-1-i] != subseg.tuple[subseg.num_points-1-i]:
			return 0
		i=i+1
	return 1

"""
input:Point poi
output: the control point, the path to seg , the seg,seg to cp,seg to the other . store in a list
if not found , return an empty list
wangxing:2010-5-23
"""
def getMinCP(poi):
	cpdebug = 0
	if cpdebug == 1:
		print "get min cp begin"

	seglist = RoadSegmentDB.objects.all()
	mindist = 1000000
	result = []
	minseg = LineString((0,0),(0,0))
	i = 1
	for seg in seglist:
		#tmpresult = getCP(poi,seg.tuple[0],seg.tuple[1])
		tmpresult = _point2Seg(poi,seg.geom)
		#get the control point and path
		if tmpresult != []:
			if tmpresult[1].length < mindist:
				result = tmpresult
				mindist = tmpresult[1].length
				minseg = seg.geom
	
	ret = []
	ret.append(result[0])#control point
	ret.append(result[1])#path to seg
	ret.append(minseg)
	ret.append(result[2])#path to cp
	ret.append(result[3])#path to the other end
	return ret	

"""
input: query point , segment(LineString) 
output: the control point , the path to segment,path to cp,path to the other end
if invalid , return an empty list
wangxing:2010-5-25:create
note:
1.whether mindist is suitable
"""
def _point2Seg(poi,seg):	
	#print "point 2 segment"

	mindist = 100000
	minpath = LineString((0,0),(0,0))
	minindex = -1
	
	#get the min path
	i = 1
	while i < seg.num_points:
	#	print "line"
	#	print i
		liner = _point2Line(poi,Point(seg.tuple[i-1]),Point(seg.tuple[i]))
		if liner == []:
			i = i+1
			continue
		if liner[0] < mindist:
			mindist = liner[0]
			minindex = i
			minpath = liner[1]
		i = i+1

	result = []
	if minindex == -1:
		return result
#	print minindex
	#get the cp
	endpt = Point(minpath.tuple[1])
	pl1 = []
	i = 0
	while i < minindex:
		pl1.append(seg.tuple[i])
		i = i+1
	pl1.append(endpt.tuple)
	ls1 = LineString(pl1)

	pl2 = []
	pl2.append(endpt.tuple)
	i = minindex
	while i < seg.num_points:
		pl2.append(seg.tuple[i])
		i = i+1
	#print json.dumps(pl2)
	#print seg.wkt
	#print minindex

	ls2 = LineString(pl2)

	if ls1.length < ls2.length:
		result.append(seg.tuple[0])
		result.append(minpath)
		result.append(ls1)
		result.append(ls2)
	else:
		result.append(seg.tuple[seg.num_points-1])
		result.append(minpath)
		result.append(ls2)
		result.append(ls1)
	
	return result
		
"""
_point2Line
input : query point , a line
output : 
if online,return [0]
if not online,return [the length, path to the line]
if not exist,return a empty list
wangxing:2010-5-23:create
wangxing:2010-5-25:change logic for seg is a linesting
"""
def _point2Line(poi,segstart,segend):
	#print "point 2 line"
	if segstart.x <= segend.x:
		x1 = segstart.x
		y1 = segstart.y
		x2 = segend.x
		y2 = segend.y
	else:
		x2 = segstart.x
		y2 = segstart.y
		x1 = segend.x
		y1 = segend.y	
	px = poi.x
	py = poi.y
	
	#if ((y1-y2)/(x1-x2) == (y1-py)/(x1-px)):
	if (y1-y2)*(x1-px) == (y1-py)*(x1-x2):
		result1 = []
		if ((px < x1) or (px > x2)):
			return result1
		else:
			if (px-x1)>(x2-px):
				#result1.append(Point(x2,y2))
#				result1.append(math.sqrt((px-x2)*(px-x2)+(py-y2)*(py-y2)))
				result1.append(0)
				#tmpls = LineString((px,py),(x2,y2))
				tmpls = LineString((px,py),(px,py))
				result1.append(tmpls);
				return result1
			else:
				#result1.append(Point(x1,y1))
				#result1.append(math.sqrt((px-x1)*(px-x1)+(py-y2)*(py-y2)))
				result1.append(0)
				#tmpls = LineString((px,py),(x1,y1))
				tmpls = LineString((px,py),(px,py))
				result1.append(tmpls)
				return result1
	else:
		result2 = []
		tmpp = _getFoot(segstart,segend,poi)
		x = tmpp.x
		y = tmpp.y
		length = math.sqrt((px-x)*(px-x)+(py-y)*(py-y))

		#check the postion in y
		if y1 > y2:
			miny = y2
			maxy = y1
		else:
			miny = y1
			maxy = y2

		if ((x < x1) or (x > x2)):
			return result2
		elif ((y < miny) or (y > maxy)):
			return result2
		else:
			if(x-x1) > (x2-x):
				#result2.append(Point(x2,y2))
				#result2.append(math.sqrt((x2-x)*(x2-x)+(y2-y)*(y2-y))+length)
				result2.append(length)
				#tmpls = LineString((px,py),(x,y),(x2,y2))
				tmpls = LineString((px,py),(x,y))
				result2.append(tmpls)
				return result2
			else:	
				#result2.append(Point(x1,y1))
				#result2.append(math.sqrt((x1-x)*(x1-x)+(y1-y)*(y1-y))+length)
				result2.append(length)
				#tmpls = LineString((px,py),(x,y),(x1,y1))
				tmpls = LineString((px,py),(x,y))
				result2.append(tmpls)
				return result2

"""
input:line defined by p1,p2 , the out point outp
output:foot of a perpendicular
wangxing:2010-5-25
testcase:
(1,1)(1,2)(1.5,1.5)->(1,1.5)
(1,1)(2,1)(1.5,1.5)->(1.5,1)
(1,1)(2,2)(1,2)->(1.5,1.5)
"""
def _getFoot(p1,p2,outp):
	x1 = p1.x
	y1 = p1.y
	x2 = p2.x
	y2 = p2.y
	ox = outp.x
	oy = outp.y

	if x1 == x2:
		return Point(x1,oy)
	elif y1 == y2:
		return Point(ox,y1)
	else:
		k = (y2-y1)/(x2-x1)
		fx = (k*k*x1+k*(oy-y1)+ox)/(k*k+1)
		fy = k*(fx-x1)+y1
		return Point(fx,fy)

def getRoute(request):
	"""
	API method
	get the route specified by the start point and end point
	Two parameters 'start' and 'end' are shipped with request.
	They are start point and end point coordinates represented as WKT strings.
	
	Return: (a json object)
	{
		path:value,wkt representation of the path
		desc:value, text description of the route
	}
	"""

	print "query route request started"
	floatRe = re.compile('([-+]?[0-9]*\.?[0-9]+)')
	start = request.REQUEST['start']
	start_list = floatRe.findall(start)
	startPt = Point(float(start_list[0]),float(start_list[1]))
	print "startPt", startPt

	end = request.REQUEST['end']
	end_list = floatRe.findall(end)
	endPt = Point(float(end_list[0]),float(end_list[1]))
	print "endPt", endPt

	return HttpResponse(getRouteCache(startPt,endPt))

def getRouteCache(startPt,endPt):
	routebegintime = time.time()
	routequerystr = "route"+str(startPt)+str(endPt)
#	print routequerystr
	routequerystr = routequerystr.replace(" ","")
	stre = cache.get(routequerystr)
	if stre != None:
		routeendtime = time.time()
		print routeendtime-routebegintime
		return stre

	route = getRoutePP(startPt,endPt)

#	print "query route is:", route
	
	path_list = []
	path_entry = {}	
	path_entry["path"] = route.wkt
	path_entry["desc"] = ""
	path_list.append(path_entry)
	
	stre = json.dumps(path_list)
	cache.set(routequerystr,stre,60*15)
	routeendtime = time.time()
	print routeendtime-routebegintime

	return stre



def createRoadNet(request):
	"""
	API method
	
	create RoadNet instance with road data from database table roaddb
	"""
	#read road data from database
	roadDBList = RoadDB.objects.all()
	roadList = []
	for roadDB in roadDBList:
		attr = {}
		attr['name'] = roadDB.name
		attr['pk'] = roadDB.pk
		road = Road(roadDB.geom, attr)
		roadList.append(road)
	
	#genreate roadnet
	roadNet = RoadNet(roadList)
	
	
	#empty RoadSegmentDB
	for rsdb in RoadSegmentDB.objects.all():
		rsdb.delete()
		
	#save road segment to database
	rsList = roadNet.getRoadSegmentList()
	for rs in rsList:
		obj_road =  RoadDB.objects.get(pk = rs[1])
		obj = RoadSegmentDB(geom = rs[0], road = obj_road)
		obj.save()
	
	#empty ControlPointDB
	for cpdb in ControlPointDB.objects.all():
		cpdb.delete()	

	index = 0
        for cp in roadNet.getControlPointList():
        	obj = ControlPointDB(geom=cp, vertex_id = index)
		index = index + 1
		obj.save()
	#empty RouteDB
	for routedb in RouteDB.objects.all():
		routedb.delete()
	
	#save route to database
	routeList = roadNet.getRouteList()
	for route in routeList:
		tmpdesc = route.attributes['desc']
		if len(tmpdesc) > 300:
			tmpdesc = tmpdesc[0:290]+"..."
		tmpdesc = ""
		routeGeom = route.geom
		cp = Point(route.geom[0])
		startPt = ControlPointDB.objects.filter(geom=cp)
		cp = Point(route.geom[-1])
		endPt = ControlPointDB.objects.filter(geom=cp)
		obj = RouteDB(geom = route.geom, desc=tmpdesc,startPt=startPt[0], endPt=endPt[0])
		#obj = RouteDB(geom = route.geom, desc=route.attributes['desc'])
		obj.save()
		

def importRoad(request):
	"""
	API method
	save road files to the database as Model RoadDB

	A shape file is shipped with request which could be accessed by request.FILES['road']
	all linestring data included in the shapefile would be saved to database
	"""
	#receive shape file and save it in a temp file folder
	fileData = request.FILES['road'].read()
	fileName = request.FILES['road'].name	
	pass

def _importRoadShapeFile(filePath):
	ds = DataSource(filePath)
	lyr = ds[0]
	
	#empty RoadDB
	for obj in RoadDB.objects.all():
		obj.delete()
	
	for feat in lyr:
		obj = RoadDB(geom=LineString(feat.geom.tuple), name=feat.get('name'))
		obj.save()
