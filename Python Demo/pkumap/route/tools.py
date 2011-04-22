# encoding: utf-8
"""
Summary: small tools for spatial operation
"""
from django.contrib.gis.geos import LineString
from django.contrib.gis.gdal import DataSource
import math
from osgeo import ogr

def roadSegmentToText(lineString, direction = True):
    """
        convert the lineString of the road segment into text description
        
        input:
            lineString: describes the road segement
            direction: boolean variable indicating the direction
            True means same direction as lineString
            False means reverse direction as lineString
        return:
            a string including the text description
    """    
    sPt = lineString.coords[0]
    ePt = lineString.coords[-1]
    
    if direction is not True:
        temp = ePt
        ePt = sPt
        sPt = temp
    
    orientation = math.atan2(ePt[1] - sPt[1], ePt[0] - sPt[0]) 
    distance = lineString.length
    
    #determine orientation
    if orientation >= -math.pi / 4 and orientation < math.pi / 4:
        orientation = '东'
        
    elif orientation >= math.pi / 4 and orientation < 3 * math.pi / 4:
        orientation = '北'
        
    elif orientation >= 3 * math.pi / 4 and orientation < math.pi:
        orientation = '西'
                
    else:
        orientation = '南'
        
    #generate text
    desc = '向 %(oriet)s 步行 %(dist)d 米' % {'oriet':orientation, 'dist':int(distance)} 
    
    return desc

def multiLineStringToLineString(original, desc):
    """
    convert a shape file with geometry type of multilinestring to a new 
    shape file with geometry type of linestring
    input:
        original, the file path of multiplinestring shapefile
        desc, the file path of new linestring shapefile
    return 
        None
    """
    oriDs = DataSource(original)
    
    driverName = "ESRI Shapefile"
    drv = ogr.GetDriverByName( driverName )    
    newDs = drv.CreateDataSource(desc)
    
    layerName = "split_road"
    newLyr = newDs.CreateLayer(layerName, None, ogr.wkbLineString)
    field_defn = ogr.FieldDefn( "Name", ogr.OFTString ) 
    field_defn.SetWidth( 32 )
    newLyr.CreateField ( field_defn )
    
    oriLyr = oriDs[0]    
    for feat in oriLyr:
        geom = feat.geom
        for subGeom in geom:
            feat = ogr.Feature(newLyr.GetLayerDefn())
            newGeom = ogr.CreateGeometryFromWkt(subGeom.wkt)
            feat.SetGeometry(newGeom)
            newLyr.CreateFeature(feat)
    
    newDs.Destroy()