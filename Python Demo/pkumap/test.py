import sys
import settings
from route.models import ControlPointList
from route.models import RoadNet
from route.views import createRoadNet
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
import cProfile


if __name__ == "__main__":
	print "----------------", "test begin: create roadnet", "----------------"
	#cProfile.run("createRoadNet('a')",'createRoadNet.profile')
	createRoadNet('a')
	print "----------------", "test finish: create roadnet", "----------------"
	