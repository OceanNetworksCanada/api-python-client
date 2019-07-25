#-------------------------------------------------------------------------------
# Name:        ags
# Purpose:     This class provides access to the ONC ArcGIS Server REST API
#
# Author:      ryanross
#
# Created:     1/2/2017
# Copyright:   (c) Ocean Networks Canada 2016
# Licence:     None
# Requires:    requests library - [Python Install]\scripts\pip install requests
#-------------------------------------------------------------------------------

import requests
import json
import math
from datetime import datetime
import os.path
import sys
from contextlib import closing
import time
import uuid
#import arcpy


class AGS:
    baseUrl = "https://ncarcgis.onc.uvic.ca:6443/arcgis/rest/services/"

    def __init__(self,baseUrl):
        self.baseUrl = baseUrl

    def queryLayerREST(self,map,layer,parameters):
        url='{0}{1}/MapServer/{2}/query'.format(self.baseUrl,map,layer)
        
        response = requests.get(url,params=parameters, verify=False)
        if (response.ok):
            result = json.loads(str(response.content,'utf-8'))
            
            features = result['features']
            if len(features) == 0:
                print('No records found')
                return None
            
            flds = ','.join([fld['alias'] for fld in result['fields']])
            
            if 'geometry' in features[0]:
                flds = '{},latitude,longitude'.format(flds)
                
            print(flds)
            print(' ')
            
            for feat in features:
                a = feat['attributes']
                attr = ','.join(["{}".format(a[fld['name']]) for fld in result['fields']])
                if 'geometry' in feat:
                     g = feat['geometry']
                     attr = '{},{},{}'.format(attr,g['y'],g['x'])
                print(attr)
                                    
                
                
                #print(a['DEVICEID'],a['DEVICENAME'],a['DEVICECATEGORYNAME'],a['LOCATIONNAME'],g['y'],g['x'])
            #print(result['features'])
        
    
#     def queryLayerArcpy(self,map,layer):
# 
#         arcpy.env.overwriteOutput = True
#         
#         where = "DEVICEID=23818"
#         fields = "*"
#         
#         srIn = arcpy.SpatialReference(4269)
#         srOut = arcpy.SpatialReference(3857)
#         rect = arcpy.Polygon(arcpy.Array([arcpy.Point(-123.5,49.05),arcpy.Point(-123.5,49.1),arcpy.Point(-123.3,49.1),arcpy.Point(-123.3,49.05),arcpy.Point(-123.5,49.05)]),srIn)
#         prjRect = rect.projectAs(srOut)
#         
#         #query = "?where={}&outFields={}&returnGeometry=true&f=json".format(where, fields)
#         geometry='{xmin: -123.3, ymin: 49.05, xmax: -123.5, ymax: 49.1}'
#         
#         
#         #https://ncarcgis.onc.uvic.ca:6443/arcgis/rest/services/ERMA/MapServer/1/query?where=&text=&objectIds=&time=&geometry=%7Bxmin%3A+-123.3%2C+ymin%3A+49.05%2C+xmax%3A+-123.5%2C+ymax%3A+49.1%7D
#         
#         query="?geometry={}&geometryType=esriGeometryEnvelope&inSR={}&spatialRel=esriSpatialRelIntersects&outFields={}&returnGeometry=true&f=json".format(geometry,4269,fields)
#         
#         #&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=html
#         
#         
#         #query = "?geometry={}&geometryType=polygon,esriGeometryEnvelope={}&outFields={}&returnGeometry=true&f=json".format(prjRect.JSON,3857,fields)
#         url='{0}{1}/MapServer/{2}/query{3}'.format(self.baseUrl,map,layer,query)
#         
#         fs = arcpy.FeatureSet()
#         fs.load(url)
#         
#         arcpy.CopyFeatures_management(fs, "c:/temp/devices.shp")

