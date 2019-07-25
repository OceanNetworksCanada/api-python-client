#-------------------------------------------------------------------------------
# Name:        dap
# Purpose:     This class provides access to the ONC ERDDAP implementation of OPeNDAP
#
# Author:      ryanross
#
# Created:     31/10/2016
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
if sys.version_info.major == 2:
    from V2 import util
else:
    from onc.V3 import util
    
#from html.parser import HTMLParser


m_baseUrl = "http://qaweb2.neptune.uvic.ca/api/"
m_method = "get"
m_token = 'YOUR_TOKEN_HERE'

m_info = False
# m_outPath = 'c:/temp'


#####################
##     ERDDAP      ##
#####################
class ERDDAP:
    baseUrl = "http://dap.onc.uvic.ca/"
    showInfo = False
    outPath = 'c:/temp'

    def __init__(self, production=True,showInfo=False,outPath='c:/temp'):
        if production:
            self.baseUrl = "http://dap.onc.uvic.ca/"
        else:
            self.baseUrl = "http://qadap.onc.uvic.ca/"
        self.showInfo = showInfo
        self.pyVersion = sys.version_info.major
        self.outPath = outPath
        
    def writeDataset(self, datasetName,extension,parameters):
        url = '{0}erddap/tabledap/{1}.{2}'.format(self.baseUrl,datasetName,extension,parameters)
    
    
        filePath = '{}/{}.{}'.format(self.outPath,datasetName,extension)
        print ("Downloading {}.{}".format(datasetName,extension))
        #downloadParameters = 'timeseries_id,time,Sound_Speed,pitch,roll,temperature,pressure,latitude,longitude,depth&time%3E=2014-09-27T00:00:00.000Z&time%3C=2014-09-28T00:00:00.000Z'
        with open(filePath,'wb') as handle:
            with closing(requests.get(url,params=parameters,stream=True)) as streamResponse:
                if (streamResponse.ok):
                    try:
                        for block in streamResponse.iter_content(1024):
                            handle.write(block)
                    except KeyboardInterrupt:
                        print('Process interupted: Deleting {}'.format(filePath))
                        handle.close()
                        streamResponse.close()
                        os.remove(filePath)
                        sys.exit(-1)
                else:
                    print("  Unable to download dataset")
#                     parser = erddapHTMLParser()
#                     parser.feed(str(streamResponse.content,'utf-8'))
        return filePath
    
    def getDataset(self, datasetName,extension,parameters):
        url = '{0}erddap/tabledap/{1}.{2}'.format(self.baseUrl,datasetName,extension,parameters)
    
        filePath = '{}/{}.{}'.format(self.outPath,datasetName,extension)
    
        print ("Retrieving {}.{}".format(datasetName,extension))
        #parameters = 'time,temperature,pressure&time%3E=2014-09-27T00:00:00.000Z&time%3C=2014-09-27T00:00:30.000Z'
        response = requests.get(url,params=parameters)
        if (response.ok):
            payload = json.loads(str(response.content,'utf-8'))
            #print(payload)
            table = payload['table']
            if (table):
                columnNames = table['columnNames']
                columnTypes = table['columnTypes']
                rows = table['rows']
                for row in rows:
                    s = []
                    for i in range(0,len(row)):
                        s.append('{}: {}'.format(columnNames[i],row[i]))
        ##                if(columnTypes[i] == 'String'):
        ##                    s.append('"{}":"{}"'.format(columnNames[i],row[i]))
        ##                else:
        ##                    s.append('"{}":{}'.format(columnNames[i],row[i]))
        
                    print ('  {}'.format(', '.join(s)))
        else:
            print("  Unable to load dataset")
            parser = erddapHTMLParser()
            parser.feed(str(response.content,'utf-8'))
                        
    
        return True

# 
# class erddapHTMLParser(HTMLParser):
#     foundLabel = False
#     foundText = False
#     Label = None
#     Text = None
#     def handle_starttag(self, tag, attrs):
#         if tag=='b': self.foundLabel = True
#         if tag=='u': self.foundText = True
#         #print("Encountered a start tag:", tag)
#   
#     def handle_endtag(self, tag):
#         if tag=='b': self.foundLabel = False
#         if tag=='u': self.foundText = False
#         #print("Encountered an end tag :", tag)
# 
#     def handle_data(self, data):
#         if self.foundLabel:self.Label = data
#         if self.foundText:self.Text = data
#         if self.Label and self.Text: 
#             print("    {0}  : {1}".format(self.Label,self.Text))
#             self.Label=None
#             self.Text=None


