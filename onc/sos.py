#-------------------------------------------------------------------------------
# Name:        onc
# Purpose:     This class provides access to the ONC Sensor Observation Service (SOS)
#
# Author:      ryanross
#
# Created:     31/10/2016
# Copyright:   (c) Ocean Networks Canada 2016
# Licence:     None
# Requires:    Python 3+
#              requests library - [Python Install]\scripts\pip install requests
#              xmljson  library - [Python Install]\scripts\pip install xmljson
#-------------------------------------------------------------------------------
import sys
if sys.version_info.major == 2:
    from V2 import util
else:
    from onc.V3 import util
    
import requests
import json
from xml.etree.ElementTree import fromstring
import math
from datetime import datetime

import xmljson
from collections import OrderedDict

sensorML = '{http://www.opengis.net/sensorML/1.0.1}'
ows = '{http://www.opengis.net/ows/1.1}'
swe='{http://www.opengis.net/swe/1.0.1}'
om='{http://www.opengis.net/om/1.0}'
gml='{http://www.opengis.net/gml}'
xlink='{http://www.w3.org/1999/xlink}'
sos='{http://www.opengis.net/sos/1.0}'

class SOS:
    baseUrl = "http://dmas.uvic.ca/"
    showInfo = False

    def __init__(self, production=True,showInfo=False):
        if production:
            self.baseUrl = "http://dmas.uvic.ca/"
        else:
            self.baseUrl = "http://qaweb2.neptune.uvic.ca/"
        self.showInfo = showInfo
        self.pyVersion = sys.version_info.major

    #SOS - Sensor Observation Service methods
    
    def getCapabilities_SOAP(self):
        url='{}sos?WSDL'.format(self.baseUrl)
        headers = {'content-type': 'application/soap+xml'}
        #headers = {'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="UTF-8"?>
                    <GetCapabilities xmlns="http://www.opengis.net/sos/1.0"
                    	xmlns:ows="http://www.opengis.net/ows/1.1"
                    	xmlns:ogc="http://www.opengis.net/ogc"
                    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    	xsi:schemaLocation="http://www.opengis.net/sos/1.0
                    	http://schemas.opengis.net/sos/1.0.0/sosGetCapabilities.xsd"
                    	service="SOS">
    
                    	<ows:AcceptVersions>
                    		<ows:Version>1.0.0</ows:Version>
                    	</ows:AcceptVersions>
    
                    	<ows:Sections>
                    		<ows:Section>ServiceIdentification</ows:Section>
                    		<ows:Section>ServiceProvider</ows:Section>
                    		<ows:Section>OperationsMetadata</ows:Section>
                    		<ows:Section>Filter_Capabilities</ows:Section>
                    		<ows:Section>Contents</ows:Section>
                    	</ows:Sections>
                    </GetCapabilities>"""
        
        sensors = []
        
        start = datetime.now()
        response = requests.post(url,data=body,headers=headers)
        end = datetime.now()
    
        if (response.ok):
            print('SOS Capabilities')
            payload = fromstring(response.content)
            
            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
                       
            operation = dict['{0}Capabilities'.format(sos)]['{0}OperationsMetadata'.format(ows)]['{0}Operation'.format(ows)]
            
            gc = [o for o in operation if o['@name']=='GetCapabilities'][0]
            go = [o for o in operation if o['@name']=='GetObservation'][0]
            ds = [o for o in operation if o['@name']=='DescribeSensor'][0]
            
            prm = ds['{0}Parameter'.format(ows)]
            p = [p for p in prm if p['@name']=='procedure'][0]
            av = p['{0}AllowedValues'.format(ows)]
            values = av['{0}Value'.format(ows)]
            for val in [v['$'] for v in values]:
                valDef = val.split(':')
                value = valDef[len(valDef)-1]
                sensors.append(value)
                if self.showInfo:print(value)
    
        else:
            util.printErrorMessage(response,{})
            return False
    
        util.printResponseTime(end,start)
    
        return sensors
    
    def getCapabilities_KVP(self,parameters={}):
        sensors = []
        offerings = []
        url='{}sos'.format(self.baseUrl)
    
        parameters['service'] = 'SOS'
        parameters['request'] = 'GetCapabilities'
    
        start = datetime.now()
        response = requests.get(url,params=parameters)
        end = datetime.now()
    
    
        if (response.ok):
            if self.showInfo:print('SOS Capabilities')
            payload = fromstring(response.content)
            
            print(payload)

            
#             BadgerFish: Use "$" for text content, @ to prefix attributes
#             GData: Use "$t" for text content, attributes added as-is
#             Yahoo Use "content" for text content, attributes added as-is
#             Parker: Use tail nodes for text content, ignore attributes

            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
                       
            operation = dict['{0}Capabilities'.format(sos)]['{0}OperationsMetadata'.format(ows)]['{0}Operation'.format(ows)]
            
            gc = [o for o in operation if o['@name']=='GetCapabilities'][0]
            
            
            ds = [o for o in operation if o['@name']=='DescribeSensor'][0]
            prm = ds['{0}Parameter'.format(ows)]
            p = [p for p in prm if p['@name']=='procedure'][0]
            av = p['{0}AllowedValues'.format(ows)]
            values = av['{0}Value'.format(ows)]
            for val in [v['$'] for v in values]:
                valDef = val.split(':')
                value = valDef[len(valDef)-1]
                sensors.append(value)
                if self.showInfo:print(value)
                
            go = [o for o in operation if o['@name']=='GetObservation'][0]
            prm = go['{0}Parameter'.format(ows)]
            p = [p for p in prm if p['@name']=='offering'][0]
            av = p['{0}AllowedValues'.format(ows)]
            values = av['{0}Value'.format(ows)]
            for val in [v['$'] for v in values]:
                valDef = val.split('Offering')
                value = valDef[len(valDef)-1]
                offerings.append(value)
            
            

    
        else:
            util.printErrorMessage(response,parameters)
            return False
    
        if self.showInfo:util.printResponseTime(end,start)
    
        return {"sensors":sensors,"offerings":offerings}
    
    
    def describSensor_SOAP(self,sensor):
        deviceInfo = {}
        url='{}sos?WSDL'.format(self.baseUrl)
        headers = {'content-type': 'application/soap+xml'}
        #headers = {'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="UTF-8"?>
                <DescribeSensor version="1.0.0" service="SOS"
                	xmlns="http://www.opengis.net/sos/1.0"
                	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                	xsi:schemaLocation="http://www.opengis.net/sos/1.0
                	http://schemas.opengis.net/sos/1.0.0/sosDescribeSensor.xsd"
                	outputFormat="text/xml;subtype=&quot;sensorML/1.0.1&quot;">
    
                	<procedure>urn:ogc:def:sensor:{0}</procedure>
    
                </DescribeSensor>""".format(sensor)
        start = datetime.now()
        response = requests.post(url,data=body,headers=headers)
        end = datetime.now()
    
        if (response.ok):
            if self.showInfo:print('SOS Describe Sensor')
            payload = fromstring(response.content)

            
#             BadgerFish: Use "$" for text content, @ to prefix attributes
#             GData: Use "$t" for text content, attributes added as-is
#             Yahoo Use "content" for text content, attributes added as-is
#             Parker: Use tail nodes for text content, ignore attributes

            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
            
            member = dict['{0}SensorML'.format(sensorML)]['{0}member'.format(sensorML)]['{0}System'.format(sensorML)]
            keywords = member['{0}keywords'.format(sensorML)]['{0}KeywordList'.format(sensorML)]
            
            #Get the Short Name, Long Name and Unique Identifier
            identifiers = member['{0}identification'.format(sensorML)]['{0}IdentifierList'.format(sensorML)]
            for i in identifiers['{0}identifier'.format(sensorML)]:
                term = i['{0}Term'.format(sensorML)]['@definition']
                value = i['{0}Term'.format(sensorML)]['{0}value'.format(sensorML)]['$']
                idDef = term.split(':')
                id = idDef[len(idDef)-1]
                valDef = value.split(':')
                val = valDef[len(valDef)-1]
                deviceInfo[id] = val

            #Get the Sensor Name and ID
            sensors = {}
            inputs = member['{0}inputs'.format(sensorML)]['{0}InputList'.format(sensorML)]
            if ('{0}input'.format(sensorML) in inputs):
                for i in inputs['{0}input'.format(sensorML)]:
                    name = i['@name']
                    sensorDef = i['{0}ObservableProperty'.format(swe)]['@definition'].split(':')
                    sensorId = sensorDef[len(sensorDef)-1]
                    if self.showInfo:print('    {} ({})'.format(name,sensorId))
                    sensors[sensorId] = name

            deviceInfo['sensors'] = sensors

    
        else:
            util.printErrorMessage(response,{})
            return False
    
        if self.showInfo:util.printResponseTime(end,start)
        
        return deviceInfo
    
    
    def getObservation_SOAP(self,offering,begin,end,observedProperty,propertyDictionary={}):
        result = {}
        url='{}sos?WSDL'.format(self.baseUrl)
        headers = {'content-type': 'application/soap+xml'}
        #headers = {'content-type': 'text/xml'}
        observedProperties = '\n'.join(['                    <observedProperty>urn:ogc:def:phenomenon:{}</observedProperty>'.format(p) for p in observedProperty])
        
        body = """<?xml version="1.0" encoding="UTF-8"?>
                <GetObservation xmlns="http://www.opengis.net/sos/1.0"
                	xmlns:ows="http://www.opengis.net/ows/1.1"
                	xmlns:gml="http://www.opengis.net/gml"
                	xmlns:ogc="http://www.opengis.net/ogc"
                	xmlns:om="http://www.opengis.net/om/1.0"
                	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                	xsi:schemaLocation="http://www.opengis.net/sos/1.0
                	http://schemas.opengis.net/sos/1.0.0/sosGetObservation.xsd"
                	service="SOS" version="1.0.0" srsName="urn:ogc:def:crs:EPSG::4326">
    
                	<offering>Offering{0}</offering>
    
                	<eventTime>
                		<ogc:TM_During>
                			<ogc:PropertyName>om:samplingTime</ogc:PropertyName>
                			<gml:TimePeriod>
                				<gml:beginPosition>{1}</gml:beginPosition>
                				<gml:endPosition>{2}</gml:endPosition>
                			</gml:TimePeriod>
                		</ogc:TM_During>
                	</eventTime>
                	{3}
                	<responseFormat>text/xml;subtype=&quot;om/1.0.0&quot;</responseFormat>
                </GetObservation>""".format(offering,begin,end,observedProperties)
        
        print(body)
        start = datetime.now()
        response = requests.post(url,data=body,headers=headers)
        end = datetime.now()
    
        if (response.ok):
            
            if self.showInfo:print('SOS Get Observation')
            payload = fromstring(response.content)
            
            print(payload)

            
#             BadgerFish: Use "$" for text content, @ to prefix attributes
#             GData: Use "$t" for text content, attributes added as-is
#             Yahoo Use "content" for text content, attributes added as-is
#             Parker: Use tail nodes for text content, ignore attributes

            bf = xmljson.BadgerFish()
            dict = bf.data(payload)

            fields = []
            observations = []
            
            if '{0}ExceptionReport'.format(ows) in dict.keys():
                exceptionReport = dict['{0}ExceptionReport'.format(ows)]
                exception = exceptionReport['{0}Exception'.format(ows)]
                print(exception['{http://www.opengis.net/ows/1.1}ExceptionText']['$'])
                return result
                
            oc = dict['{0}ObservationCollection'.format(om)]
            id = oc['@{0}id'.format(gml)]
            result['id']=id
            
            member = oc['{}member'.format(om)]
            try:
                if member['@{http://www.w3.org/1999/xlink}href'] =='urn:ogc:def:nil:OGC:inapplicable':
                    print('There is no data for device and time range')
                    return result
            except:
                pass
                
            observation = member['{0}Observation'.format(om)]
            idGo = observation['@{0}id'.format(gml)]
            #samplingTime = observation['{0}samplingTime'.format(om)]
            timePeriod = observation['{0}samplingTime'.format(om)]['{0}TimePeriod'.format(gml)]
            timePeriodType = timePeriod['@{http://www.w3.org/2001/XMLSchema-instance}type']
            beginPosition = timePeriod['{0}beginPosition'.format(gml)]['$']
            endPosition = timePeriod['{0}endPosition'.format(gml)]['$']
            result['samplingTime']={"begin":beginPosition,"end":endPosition}
            
            procedure = observation['{0}procedure'.format(om)]['@{0}href'.format(xlink)]
            #observedProperty = observation['{0}observedProperty'.format(om)]['@{0}href'.format(xlink)]
            cp = observation['{0}observedProperty'.format(om)]['{0}CompositePhenomenon'.format(swe)]
            cpName = cp['{0}name'.format(gml)]['$']
            cpLink = []
            for c in cp['{0}component'.format(swe)]:
                cpLink.append(c['@{0}href'.format(xlink)])
            
            result['CompositePhenomenon'] = {"name":cpName,"components":cpLink}
            
            foiTitle = observation['{0}featureOfInterest'.format(om)]['@{0}title'.format(xlink)]
            foiLink = observation['{0}featureOfInterest'.format(om)]['@{0}href'.format(xlink)]
            
            result['featureOfInterest']=foiTitle
            
            dataArray = observation['{0}result'.format(om)]['{0}DataArray'.format(swe)]
            elementCount = dataArray['{0}elementCount'.format(swe)]['{0}Count'.format(swe)]['{0}value'.format(swe)]['$']
            elementType = dataArray['{0}elementType'.format(swe)]
            for f in elementType['{0}DataRecord'.format(swe)]['{0}field'.format(swe)]:
                name = f['@name']
                fields.append(name)
            if self.showInfo:print(fields)
            
            
            
            encoding = dataArray['{0}encoding'.format(swe)]['{0}TextBlock'.format(swe)]
            decimalSeparator = encoding['@decimalSeparator']
            tokenSeparator = encoding['@tokenSeparator']
            blockSeparator = encoding['@blockSeparator']
            values = dataArray['{0}values'.format(swe)]['$'].split(blockSeparator)
            for v in values:
                observation = {} #OrderedDict()
                o = v.split(tokenSeparator)
                if len(o)==len(fields):
                    for i in range(0,len(fields)):
                        field = str(fields[i])
                        if (field in propertyDictionary.keys()):
                            field = propertyDictionary[field]
                            observation[field] = float(o[i])
                        else:
                            observation[field] = o[i]
                            
                    if self.showInfo:print(v)
                    if self.showInfo:print(observation)
                    observations.append(observation)

            result['observations']=observations
        else:
            util.printErrorMessage(response,{})
            return False
    
        if self.showInfo:util.printResponseTime(end,start)
        return result
    
    
    


