# encoding: utf-8
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import MultiPoint
from django.contrib.gis.geos import LineString
import networkx as nx
import sys
import tools

verbose = True

class RoutePoiDB(models.Model):
	name = models.CharField(max_length=20)
	alias = models.CharField(max_length=100)#another names,divide by blackspace
	geom = models.PointField()
	searchcount = models.IntegerField()#hot value
	objects = models.GeoManager()

	def __unicode__(self):
		return self.name

class ControlPointDB(models.Model):
    geom = models.PointField()
    vertex_id = models.IntegerField()
    objects = models.GeoManager()
    
class RoadDB(models.Model):
    name = models.CharField(max_length=20)
    geom = models.LineStringField()
    objects = models.GeoManager()

class RouteDB(models.Model):
    desc = models.CharField(max_length=2000)
    geom = models.LineStringField()
    objects = models.GeoManager()
    startPt = models.ForeignKey(ControlPointDB,related_name="start_pt")
    endPt = models.ForeignKey(ControlPointDB, related_name="end_pt")
    
class RoadSegmentDB(models.Model):
    road = models.ForeignKey(RoadDB)
    geom = models.LineStringField()
    objects = models.GeoManager()

class Road:
    """
        class represents memory structure of road
    """
    def __init__(self, geom, attributes):
        """
        type(geom): django.contrib.gis.geos.LineString
        type(attributes): dictionary,
        the specific values in the dictionary are defined by design document
        """
        self.geom = geom
        self.attributes = attributes

class Route:
    """
        memory class for representing Route Model
    """
    def __init__(self, geom, attributes):
        """
        type(geom): django.contrib.gis.geos.LineString
        type(attributes): dictionary,
        the specific values in the dictionary are defined by design document
        """
        self.geom = geom
        self.attributes = attributes

       
class ControlPointList(list):
    def __init__(self, tolerance = 0.1):
        self.data = []
        self.tolerance = tolerance
    
    def __str__(self):
        str = "["
        for pt in self:
            str = str + pt.__str__()
        str = str + "]"
        return str
    
    def append(self, cPt):
        """
        override default list append method
        restriction:
        type(cPt) == django.contrib.gis.geos.Point
        
        besides, points in the list should be mutex 
        if dist(pt1, pt2) < tolerance,
        then we consider them as same points
        """        
        if type(cPt) is not Point:
            raise Exception('Type must be django.controib.gis.geos.Point', 'eggs')
        for pt in self:
            if pt.distance(cPt) < self.tolerance:
                return
        list.append(self,cPt)
    
    def extend(self,cPts):
        """
        override default list extend method
        restriction:
        each item in Cpts should satisfy  
        type(item) == django.contrib.gis.geos.Point
        
        besides, points in the list should be mutex 
        if dist(pt1, pt2) < tolerance,
        then we consider them as same points
        """
        for cPt in cPts:
            flag = False
            for pt in self:                
                if pt.distance(cPt) < self.tolerance:
                    flag = True
                    cPt[0] = pt[0]
                    cPt[1] = pt[1]
                    break
            if flag == False:
                list.append(self, cPt)

    def index(self, cPt):
    	for i in range(len(self)):
		if self[i].distance(cPt) < self.tolerance:
			return i
	
	raise ValueError
                
class RoadSegmentList(list):
    def __init__(self):
        self.data = []
        self.tolerance = 1.5
        
    def fetch(self, sPt,ePt):
        tolerance = self.tolerance
        for rs in self:
            rs_spt = Point(rs[0].coords[0])
            rs_ept = Point(rs[0].coords[-1])            
            if ((rs_spt.distance(sPt) < tolerance) and (rs_ept.distance(ePt) < tolerance)) or ((rs_spt.distance(ePt) < tolerance) and (rs_ept.distance(sPt) < tolerance)):
                return rs

        print 'RoadSegment from Point', sPt,'to', ePt, 'could not be found'
        raise ValueError
                
class RoadNet:
    """
    build topological structure of roads and calculate weighted shortest paths between
    any control points on the road net 
    """
    cpList = ControlPointList()
    rsList = RoadSegmentList()
    def __init__(self, roadList):
        """
        generate a nx.Graph object according to roads passed by the param roadList 
        
        return value: a nx.Graph
        """            
        cpList = self.cpList
        rsList = self.rsList
        roadSpList = []
        roadNum = len(roadList)
        
        for i in range(roadNum):
            li = ControlPointList()
            roadSpList.append(li)
            
        for i in range(len(roadList)):
            curRoad = roadList[i]
            startPt = Point(curRoad.geom.coord_seq.tuple[0])
            endPt = Point(curRoad.geom.coord_seq.tuple[-1])
            cpList.append(startPt)
            cpList.append(endPt)        
            for j in range(i+1,len(roadList)):
                interRoad = roadList[j]            
                splitPoints = curRoad.geom.intersection(interRoad.geom)
                if len(splitPoints) == 0:
                    #no intersection
                    pass
                elif type(splitPoints) == Point:
                    cpList.append(splitPoints)
                    roadSpList[i].append(splitPoints)
                    roadSpList[j].append(splitPoints)
                else:
                    cpList.extend(splitPoints)
                    roadSpList[i].extend(splitPoints)
                    roadSpList[j].extend(splitPoints)
        
        #generate roadSegment list         
        for i in range(roadNum):
            if len(roadSpList[i]) == 0:
                rsList.append((roadList[i].geom, roadList[i].attributes['pk']))
            else:
                rsList.extend(self._cutRoad(roadList[i],roadSpList[i]))
        
        #generate roadNet
        self.graph = nx.Graph()
        graph = self.graph
        graph.add_nodes_from(cpList)

        #define minLength of roadsegment
        MINROADSGLENGTH = 2
        
        for roadSegment in rsList:
            weight_value = roadSegment[0].length
            if weight_value < MINROADSGLENGTH:
                #the roadSegment is too short and consider as a blur                
                rsList.remove(roadSegment)
                continue            
            startPt = Point(roadSegment[0].coords[0])
            startPtIndex = cpList.index(startPt)
            endPt = Point(roadSegment[0].coords[-1])
            endPtIndex = cpList.index(endPt)          
            
            graph.add_edge(startPtIndex, endPtIndex, weight=weight_value,lineString=roadSegment[0])
        
        for node in graph.nodes():
            if len(graph[node].keys()) == 0:
                #If we remove the node from cp list, we could not maintain consistancy
                #between cpList and graph
                graph.remove_node(node)
        
        #calculate shortest path between each node
        self.routeTable = nx.shortest_path(graph, weighted=True)
        
    
    def _cutRoad(self, road, args):
        """
        cut road into roadsegments according to controlPoints
        """ 
        lineStringList = self._splitLineString(road.geom,args)
        
        rsList = []
        for lineString in lineStringList:
            #TODO: the problem here is we lack a unique index for road
            #Therefore we need to rely on the uniqueness of road name
            rsList.append((lineString, road.attributes['pk']))
        
        return rsList
        
    def _splitLineString(self, lineString, *args):
        """
        args type could be Point or list
        """
        minDist = sys.maxint
        tolerance = 0.1
        
        #split line string with a single point    
        if type(args[0]) == Point:
            splitPoint = args[0]
            startPt = lineString.coords[0]
            for i in range(1,len(lineString.coords)):
                endPt = lineString.coords[i]
                lineSeg = LineString(startPt, endPt)
                dist = lineSeg.distance(splitPoint) 
                if dist < minDist:
                    minDist = dist
                    splitIndex = i
            coords = list(lineString.coords[0:splitIndex])
            coords.append((splitPoint.coords))
            firstLineString = LineString(coords)
            coords = []        
            coords.append((splitPoint.coords))
            coords.extend(lineString.coords[splitIndex:])        
            secondLineString = LineString(coords)
            return [firstLineString, secondLineString]
        elif type(args[0]) == tuple  or type(args[0]) == list or type(args[0]) == ControlPointList:
            splitPointList = args[0]
            assert(len(splitPointList) != 0)
                        
            splitLines = self._splitLineString(lineString, splitPointList[-1])
            splitPointList.pop()
            
            spPtList1 = []
            spPtList2 = []
            for point in splitPointList:
                if splitLines[0].distance(point) < tolerance:
                    spPtList1.append(point)
                else:
                    spPtList2.append(point)
            resList = []
            if len(spPtList1) != 0:
                resList.extend(self._splitLineString(splitLines[0], spPtList1))
            else:
                resList.append(splitLines[0])
            if len(spPtList2) != 0:
                resList.extend(self._splitLineString(splitLines[1], spPtList2))
            else:
                resList.append(splitLines[1])
            return resList  
        else:
            raise 'Error, unsupported type'
    
    def _getRoute(self, i, j):
        """
        get the route from vertex i to vertex j
       	
	    if there is not route between vertex i and vertex j,
	    return None 
        return:
            Route 
        """
        try:
            cpIndices = self.routeTable[i][j]
        except:
            if verbose:
                print 'No route from ', i, ' to ', j
            return None
        
        startIndex = cpIndices[0]
        coords = []
        textRouteDesc = ""         
        for index in cpIndices[1:]:
            endIndex = index
            startPt = self.cpList[startIndex]
            endPt = self.cpList[endIndex]
            rs = self.graph[startIndex][endIndex]['lineString']
            
            #check road segment match condition
            if startPt == Point(rs.coords[0]):
                #startPt is the road segement startpt
                coords.extend(rs.coords)
                textRouteDesc = textRouteDesc + tools.roadSegmentToText(rs,0) + ','
            else:
                #startPt is the road segment endpt
                coords_num = len(rs.coords)
                #puzzle: reverse did not work, return None list
                for coord in reversed(rs.coords):
                    coords.append(coord)
                textRouteDesc = textRouteDesc + tools.roadSegmentToText(rs,1) + ','
            
            startIndex = endIndex
        routeGeom = LineString(coords)
        routeAttrs = {}
        routeAttrs['desc'] = textRouteDesc
        route = Route(routeGeom, routeAttrs)
        return route
    
    def getRouteList(self):
        """
        get all the routes between each any connected control points in the road net
        
        return:
            list<Route>
        """
        routeList = []
        cpNum = len(self.cpList)
        for i in range(cpNum):
            for j in range(cpNum):
                if i is not j:                
                    route = self._getRoute(i,j)
                    if route is not None:
                        routeList.append(route)
        return routeList
    
    def getRoadSegmentList(self):
        """
        get all the road segments 
        
        return:
            list<(linestring, roadid)>
        """
        return self.rsList
    
    def getControlPointList(self):
        """
        get all control points
        
        return:
            list<Point>
        """
        return self.cpList
