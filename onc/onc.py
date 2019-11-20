import json
import datetime
import re
from dateutil import parser
from modules._OncDiscovery import _OncDiscovery
from modules._OncDelivery  import _OncDelivery
from modules._OncRealTime  import _OncRealTime
from modules._OncArchive   import _OncArchive

class ONC:
    """
    Python ONC Api Client Library
    Common library wrapper
    """

    def __init__(self, token, production: bool=True, showInfo: bool=False, outPath: str='output', timeout: int=60):
        self.token    = re.sub('[^a-zA-Z0-9\-]+', '', token)
        self.showInfo = showInfo
        self.timeout  = timeout
        self.baseUrl  = 'https://data.oceannetworks.ca/'
        self.outPath  = ''

        # sanitize outPath
        if len(outPath) > 0:
            outPath = outPath.replace('\\', '/')
            if outPath[-1] == '/':
                outPath = outPath[:-1]
            self.outPath = outPath

        # switch to qa if needed
        if not production:
            self.baseUrl = 'https://qa.oceannetworks.ca/'

        # Create service objects
        self.discovery = _OncDiscovery(self)
        self.delivery  = _OncDelivery(self)
        self.realTime  = _OncRealTime(self)
        self.archive   = _OncArchive(self)


    def print(self, obj, filename: str=""):
        """
        Helper for printing a JSON dictionary to the console or to a file
        @filename: if present, creates the file and writes the output in it
        """
        text = json.dumps(obj, indent=4)
        if filename == '':
            print(text)
        else:
            with open(filename, 'w+') as file:
                file.write(text)


    def formatUtc(self, dateString: str='now'):
        """
        Helper that returns an ISO8601 string for the provided date string
        Most date formats are supported, as explained in: http://labix.org/python-dateutil#head-c0e81a473b647dfa787dc11e8c69557ec2c3ecd2
        A value of "now" returns the current UTC date & time
        Depends on the local system clock
        """
        if dateString == 'now':
            return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + '.000Z'
        else:
            objDate = parser.parse(dateString)
            return objDate.replace(microsecond=0).isoformat() + '.000Z'


    # PUBLIC METHOD WRAPPERS

    # Discovery methods

    def getLocations(self, filters: dict=None):
        return self.discovery.getLocations(filters)
    
    def getLocationHierarchy(self, filters: dict=None):
        return self.discovery.getLocationHierarchy(filters)
    
    def getDeployments(self, filters: dict=None):
        return self.discovery.getDeployments(filters)
    
    def getDevices(self, filters: dict=None):
        return self.discovery.getDevices(filters)
    
    def getDeviceCategories(self, filters: dict=None):
        return self.discovery.getDeviceCategories(filters)
    
    def getProperties(self, filters: dict=None):
        return self.discovery.getProperties(filters)
    
    def getDataProducts(self, filters: dict=None):
        return self.discovery.getDataProducts(filters)
    
    # Delivery methods

    def orderDataProduct(self, filters: dict, maxRetries: int=0, downloadResultsOnly: bool=False, includeMetadataFile: bool=True, overwrite: bool=False):
        return self.delivery.orderDataProduct(filters, maxRetries, downloadResultsOnly, includeMetadataFile, overwrite)
    
    def requestDataProduct(self, filters: dict):
        return self.delivery.requestDataProduct(filters)
    
    def runDataProduct(self, dpRequestId: int, waitComplete: bool=True):
        return self.delivery.runDataProduct(dpRequestId, waitComplete)
    
    def downloadDataProduct(self, runId: int, maxRetries: int=0, downloadResultsOnly: bool=False, includeMetadataFile: bool=True, overwrite: bool=False):
        return self.delivery.downloadDataProduct(runId, maxRetries, downloadResultsOnly, includeMetadataFile, overwrite)
    
    # Real-time methods

    def getDirectScalar(self, filters: dict=None, allPages: bool=False):
        # Alias for getDirectByLocation (to be eventually discontinued)
        return self.getDirectByLocation(filters, allPages)
    
    def getDirectByLocation(self, filters: dict=None, allPages: bool=False):
        return self.realTime.getDirectByLocation(filters, allPages)
    
    def getDirectByDevice(self, filters: dict=None, allPages: bool=False):
        return self.realTime.getDirectByDevice(filters, allPages)
    
    def getDirectRawByLocation(self, filters: dict=None, allPages: bool=False):
        return self.realTime.getDirectRawByLocation(filters, allPages)
    
    def getDirectRawByDevice(self, filters: dict=None, allPages: bool=False):
        return self.realTime.getDirectRawByDevice(filters, allPages)
    
    # Archive file methods

    def getListByLocation(self, filters: dict=None, allPages: bool=False):
        return self.archive.getListByLocation(filters, allPages)
    
    def getListByDevice(self, filters: dict=None, allPages: bool=False):
        return self.archive.getListByDevice(filters, allPages)
    
    def getFile(self, filename: str='', overwrite: bool=False):
        return self.archive.getFile(filename, overwrite)
    
    def getDirectFiles(self, filters: dict=None, overwrite: bool=False, allPages: bool=False):
        return self.archive.getDirectFiles(filters, overwrite, allPages)