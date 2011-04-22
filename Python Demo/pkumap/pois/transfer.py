from pyPgSQL import PgSQL
from django.contrib.gis.geos import Point
from pkumap.pois.models import CBuilding

dbhost = '162.105.17.119'
dbname = 'spatialdb'
dbuser = 'postgres'
dbpasswd = '1234abcd'

#transferbuilding()


def transferbuilding():
	try:
		cx = PgSQL.connect(host=dbhost,database=dbname,user=dbuser,password=dbpasswd)
		cu = cx.cursor()
		cu.execute('select * from description;')

		rows = cu.fetchall()
	
		for building in rows:
			bname = building['itemname']
			balias = building['textdesc']
			bphoto = building['imagedesc']
	
			bid = building['pid']
			pgsqlstr = 'select * from gazetteer where pid='+str(bid)+';'
			cu.execute(pgsqlstr)
			temprow = cu.fetchall()
			bloc = temprow[0]['footprint']
			#bloc = building['footprint']
		
			newbuilding = CBuilding()
			newbuilding.bname = bname
			newbuilding.balias = balias
			newbuilding.btype = 1
			newbuilding.baddr = 'null'
			newbuilding.bphoto = bphoto
			newbuilding.count = 0
			newbuilding.loc = bloc
			newbuilding.save()
	except StandardError,err:
		print 'error',err
	finally:
		cx.close()
		print 'connection close...'
