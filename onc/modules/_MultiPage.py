import re
import math
import weakref
from time import time
from datetime import timedelta
from ._util import _formatDuration
import dateutil.parser


# Handles data multi-page downloads (scalardata, rawdata, archivefiles)
class _MultiPage:
    def __init__(self, parent: object):
        self.parent = weakref.ref(parent)
        self.result = None


    def getAllPages(self, service: str, url: str, filters: dict):
        """
        Requests all pages from the service, with the url and filters
        Multiple pages will be downloaded until completed
        @return: Service response with concatenated data for all pages obtained
        """
        try:
            # pop archivefiles extension
            extension = None
            if service == 'archivefiles':
                if 'extension' in filters:
                    extension = filters['extension']
                    del filters['extension']
            
            # download first page
            start = time()
            response, responseTime = self._doPageRequest(url, filters, service, extension)
            rNext = response['next']

            if rNext != None:
                print("Data quantity is greater than the row limit and will be downloaded in multiple pages.")
                
                pageCount    = 1
                pageEstimate = self._estimatePages(response, service, responseTime)
                if pageEstimate > 0:
                    timeEstimate = _formatDuration(pageEstimate * responseTime)
                    print('Estimated approx. {:d} pages'.format(pageEstimate))
                    print('Estimated approx. {:s} to complete'.format(timeEstimate))

                # keep downloading pages until next is None
                print('')
                while rNext != None:
                    pageCount += 1
                    rowCount  = self._rowCount(response, service)

                    print("   ({:d} samples) Downloading page {:d}...".format(rowCount, pageCount))
                    nextResponse, nextTime = self._doPageRequest(url, rNext['parameters'], service, extension)
                    rNext = nextResponse['next']
                    
                    # concatenate new data obtained
                    self._catenateData(response, nextResponse, service)
                
                totalTime = _formatDuration(time() - start)
                print("   ({:d} samples) Completed in {:s}.".format(self._rowCount(response, service), totalTime))
                response['next'] = None

            return response
        except Exception: raise


    def _doPageRequest(self, url: str, filters: dict, service: str, extension: str=None):
        """
        Wraps the _doRequest method
        Performs additional processing of the response for certain services
        @param extension: Only provide for archivefiles filtering
        Returns a tuple (jsonResponse, duration)
        """
        if service == 'archivefiles':
            response, duration = self.parent()._doRequest(url, filters, getTime=True)
            response = self.parent()._filterByExtension(response, extension)
        else:
            response, duration = self.parent()._doRequest(url, filters, getTime=True)
        
        return response, duration


    def _catenateData(self, response:object, nextResponse: object, service: str):
        """
        Concatenates the data results from nextResponse into response
        Compatible with the row structure of different services
        """
        if service == 'scalardata':
            keys = response['sensorData'][0]['data'].keys()

            for sensorData in response['sensorData']:
                sensorCode = sensorData['sensorCode']
                
                nextSensor = next(ns for ns in nextResponse['sensorData'] if ns['sensorCode'] == sensorCode)
                for key in keys:
                    sensorData['data'][key] += nextSensor['data'][key]
        
        elif service == 'rawdata':
            for key in response['data']:
                response['data'][key] += nextResponse['data'][key]
        
        elif service == 'archivefiles':
            response['files'] += nextResponse['files']


    def _estimatePages(self, response: object, service: str, responseTime: float):
        """
        Estimates the number of pages this request will require, from the first page's response and its duration
        @param responseTime: request duration in seconds
        """
        # timespan covered by the data in the response
        pageTimespan = self._responseTimespan(response, service)
        if pageTimespan == 0:
            return 0

        # total timespan to cover
        totalBegin = dateutil.parser.parse(response['next']['parameters']['dateFrom'])
        totalEnd   = dateutil.parser.parse(response['next']['parameters']['dateTo'])
        totalTimespan = totalEnd - totalBegin

        # handle cases of very small timeframes
        pageSeconds  = max(pageTimespan.seconds, 1)
        totalSeconds = totalTimespan.seconds

        return math.ceil(totalSeconds / pageSeconds)


    def _rowCount(self, response, service: str):
        """
        Returns the number of records in the response
        """
        if   service == 'scalardata':
            return len(response['sensorData'][0]['data']['sampleTimes'])
        
        elif service == 'rawdata':
            return len(response['data']['times'])
        
        elif service == 'archivefiles':
            return len(response['files'])
        
        return 0


    def _responseTimespan(self, response, service: str):
        """
        Determines the timespan the data in the response covers
        Returns a timedelta object
        """
        # grab the first and last sample times
        if service in ['scalardata', 'rawdata']:
            if   service == 'scalardata':
                first = response['sensorData'][0]['data']['sampleTimes'][0]
                last  = response['sensorData'][0]['data']['sampleTimes'][-1]
            elif service == 'rawdata':
                first = response['data']['times'][0]
                last  = response['data']['times'][-1]
            
        elif service == 'archivefiles':
            row0 = response['files'][0]
            if isinstance(row0, str):
                regExp = "\d{8}T\d{6}\.\d{3}Z"
                reFirst = re.search(regExp, response['files'][0])
                reLast  = re.search(regExp, response['files'][-1])
                first = reFirst.group()
                last  = reLast.group()
                if reFirst is None or reLast is None or reFirst.group() == reLast.group():
                    return 0
            else:
                first = response['files'][0]['dateFrom']
                last  = response['files'][-1]['dateFrom']
        
        # compute the timedelta
        #print(first, last)
        dateFirst = dateutil.parser.parse(first)
        dateLast  = dateutil.parser.parse(last)
        return dateLast - dateFirst