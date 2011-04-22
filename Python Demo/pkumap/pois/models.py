#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
#class POI(models.Model):
#	"""docstring for ClassName"""
#	name = models.CharField(max_length=200)
#	desc = models.CharField(max_length=200)
#	url = models.CharField(max_length=200)
#	tel = models.CharField(max_length=10)
#	lon = models.FloatField()
#	lat = models.FloatField()
#
#	def __unicode__(self):
#		return self.name

class  CBuilding(models.Model):
	"""Building"""
	#normal models
	bname = models.CharField(max_length=200)
	balias = models.CharField(max_length=200)
	btype = models.IntegerField()
	baddr = models.CharField(max_length=200)
	bphoto = models.CharField(max_length=200)
	count = models.IntegerField()

	#geo models
	loc = models.PointField()
	objects = models.GeoManager()

	def __unicode__(self):
		return self.bname

class CEDepartment(models.Model):
	"""Entity Department"""
	ename = models.CharField(max_length=200)
	ealias = models.CharField(max_length=200)
	elink = models.CharField(max_length=200)
	eaddr = models.CharField(max_length=200)
	ephoto = models.CharField(max_length=200)
	elevel = models.IntegerField()
	ebid = models.ForeignKey('CBuilding')
	evid = models.ForeignKey('CVDepartment')
	count = models.IntegerField()

	def __unicode__(self):
		return self.ename

class CVDepartment(models.Model):
	"""Virtual Department"""
	vname = models.CharField(max_length=200)
	vlink = models.CharField(max_length=200)
	count = models.IntegerField()

	def __unicode__(self):
		return self.vname

class CScene(models.Model):
	"""Scene"""
	#normal models
	sname = models.CharField(max_length=200)
	salias = models.CharField(max_length=200)
	stype = models.IntegerField()
	slevel = models.IntegerField()
	sphoto = models.CharField(max_length=200)
	sdesc = models.CharField(max_length=1000)
	count = models.IntegerField()
	
	#geo models
	loc = models.PointField()
	objects = models.GeoManager()

	def __unicode__(self):
		return self.sname
